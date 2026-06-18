"""Canonical Bayesian Ideal Observer for the 2AFC spatial-cue detection task.

Single implementation used by notebooks/Appendix-BIO-Analysis.ipynb.
Do not duplicate this class elsewhere in the repo.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm


class BayesianIdealObserver:
    """
    Bayesian Ideal Observer (BIO) for the 2AFC target-detection task with a spatial cue.

    Assumptions (per trial):
      - Two angles: line1_angle (left), line2_angle (right).
      - Target-present TP=1 vs target-absent TP=0.
      - TP=0: both angles ~ N(mu_noise, sigma^2), cue random (0.5 left/right).
      - TP=1: one side S in {1,2} is target side, chosen with prob 0.5.
              x_S     ~ N(mu_target, sigma^2)
              x_other ~ N(mu_noise,  sigma^2)
              cue points to S with prob v (cue validity), otherwise to other side.
      - Condition determines validity v:
            50_50  -> 0.5
            80_20  -> 0.8
            100_0  -> 1.0
      - Prior P(TP=1) = prior_tp (default 0.5).

    This class:
      * Adds BIO columns (likelihood ratio, log LR, posterior, decisions) to a DataFrame.
      * Computes SDT metrics (accuracy, hit rate, fa rate, d', criterion) by condition.
    """

    def __init__(
        self,
        mu_target: float = 15.0,
        mu_noise: float = 5.0,
        sigma: float = 3.5,
        prior_tp: float = 0.5,
        cond_validity: dict | None = None,
    ):
        self.mu_target = mu_target
        self.mu_noise = mu_noise
        self.sigma = sigma
        self.prior_tp = prior_tp

        if cond_validity is None:
            cond_validity = {
                "50_50": 0.5,
                "80_20": 0.8,
                "100_0": 1.0,
            }
        self.cond_validity = cond_validity

    def add_bio_columns(
        self,
        df: pd.DataFrame,
        line1_col: str = "line1_angle",
        line2_col: str = "line2_angle",
        cue_col: str = "cue_points",
        cond_col: str = "condition",
        tp_col: str = "TP",
    ) -> pd.DataFrame:
        """Return a copy of df with BIO columns added.

        Added columns: bio_sigma, bio_lambda, bio_llr, bio_p_present, bio_decision.
        """
        out = df.copy()

        sigma = float(self.sigma)
        out["bio_sigma"] = sigma

        x1 = out[line1_col].to_numpy()
        x2 = out[line2_col].to_numpy()
        cue = out[cue_col].to_numpy()
        v = out[cond_col].map(self.cond_validity).to_numpy()

        delta_mu = self.mu_target - self.mu_noise
        offset = (self.mu_target**2 - self.mu_noise**2) / 2.0
        denom = sigma**2

        R1 = np.exp((delta_mu * x1 - offset) / denom)
        R2 = np.exp((delta_mu * x2 - offset) / denom)

        p_c_given_S1 = np.where(cue == 1, v, 1.0 - v)
        p_c_given_S2 = np.where(cue == 2, v, 1.0 - v)

        Lambda = R1 * p_c_given_S1 + R2 * p_c_given_S2

        eps = 1e-12
        Lambda_safe = np.maximum(Lambda, eps)
        log_Lambda = np.log(Lambda_safe)

        out["bio_lambda"] = Lambda_safe
        out["bio_llr"] = log_Lambda

        prior_tp = np.clip(self.prior_tp, 1e-6, 1 - 1e-6)
        prior_odds = prior_tp / (1.0 - prior_tp)
        log_posterior_odds = log_Lambda + np.log(prior_odds)
        posterior_odds = np.exp(log_posterior_odds)
        p_present = posterior_odds / (1.0 + posterior_odds)

        out["bio_p_present"] = p_present
        out["bio_decision"] = (log_posterior_odds > 0).astype(int)

        return out

    @staticmethod
    def _compute_sdt_metrics(
        df: pd.DataFrame,
        decision_col: str = "bio_decision",
        tp_col: str = "TP",
    ) -> pd.Series:
        n_trials = len(df)
        n_signal = (df[tp_col] == 1).sum()
        n_noise = (df[tp_col] == 0).sum()

        hits = ((df[tp_col] == 1) & (df[decision_col] == 1)).sum()
        fas = ((df[tp_col] == 0) & (df[decision_col] == 1)).sum()
        crs = ((df[tp_col] == 0) & (df[decision_col] == 0)).sum()

        accuracy = (hits + crs) / n_trials if n_trials > 0 else np.nan

        H = (hits + 0.5) / (n_signal + 1) if n_signal > 0 else np.nan
        F = (fas + 0.5) / (n_noise + 1) if n_noise > 0 else np.nan

        if np.isfinite(H) and np.isfinite(F):
            zH = norm.ppf(H)
            zF = norm.ppf(F)
            dprime = zH - zF
            criterion = -0.5 * (zH + zF)
        else:
            dprime = np.nan
            criterion = np.nan

        return pd.Series(
            {
                "n_trials": n_trials,
                "accuracy": accuracy,
                "hit_rate": H,
                "fa_rate": F,
                "dprime": dprime,
                "criterion": criterion,
            }
        )

    def compute_sdt_by_condition(
        self,
        df: pd.DataFrame,
        condition_col: str = "condition",
        decision_col: str = "bio_decision",
        tp_col: str = "TP",
    ) -> pd.DataFrame:
        """Group df by condition and return a DataFrame with SDT metrics per row."""
        grouped = (
            df.groupby(condition_col, as_index=False)
            .apply(lambda sub: self._compute_sdt_metrics(sub, decision_col, tp_col))
        )
        metrics = grouped.reset_index(drop=True)
        metrics.rename(columns={condition_col: "condition"}, inplace=True)
        metrics["who"] = "BIO"
        return metrics


__all__ = ["BayesianIdealObserver"]
