"""Consolidated data loaders for human, model, and BIO datasets.

Centralized functions to build master dataframes, avoiding duplication
across notebooks. All functions return properly formatted DataFrames
ready for analysis.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

from .config import get_paths


# ============================================================================
# HUMAN DATA LOADER
# ============================================================================
def load_human_master(data_dir: Path | None = None) -> pd.DataFrame:
    """Load and prepare human participant data across all conditions.

    Returns:
        DataFrame with columns: stimID, condition, response, side_selected,
        cue_points, line1_angle, line2_angle, valid_cue, TP, participantID, decision
    """
    if data_dir is None:
        paths = get_paths()
        data_dir = paths.data_dir

    folders = ["50_50", "80_20", "100_0"]

    human_df = pd.concat(
        [pd.read_csv(data_dir / f / "human_data.csv") for f in folders],
        ignore_index=True,
    )

    # Map condition codes to readable names
    human_df["condition"] = human_df["condition"].map(
        {"condition_1": "80_20", "condition_2": "50_50", "condition_3": "100_0"}
    )

    # Keep desired columns and order
    cols = [
        "stimID",
        "condition",
        "response",
        "side_selected",
        "cue_points",
        "line1_angle",
        "line2_angle",
        "valid_cue",
        "TP",
        "participantID",
    ]
    human_df = human_df[cols]

    # Binary decision from confidence rating (threshold 4)
    human_df["decision"] = (human_df["response"] >= 4).astype(int)

    return human_df


# ============================================================================
# MODEL DATA LOADER
# ============================================================================
def load_model_master(data_dir: Path | None = None) -> pd.DataFrame:
    """Load and prepare model decision data across all conditions.

    Uses decisions_fixed/ directory only. Filters bad models (0 responses).

    Returns:
        DataFrame with columns: stimID, condition, side_selected, cue_points,
        line1_angle, line2_angle, valid_cue, TP, response, participantID, decision
    """
    if data_dir is None:
        paths = get_paths()
        data_dir = paths.data_dir

    conds = ["50_50", "80_20", "100_0"]
    dfs = []

    def load_decisions(path: Path, cond: str, model_name: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        df["stimID"] = df["image_id"]
        df["condition"] = cond
        df["participantID"] = model_name
        df["response"] = (
            df["GPT_response"]
            .astype(str)
            .str.strip()
            .str.lower()
            .replace({"true": "present", "false": "absent"})
        )
        df["decision"] = df["response"].map({"present": 1, "absent": 0})
        return df[
            [
                "stimID",
                "condition",
                "side_selected",
                "cue_points",
                "line1_angle",
                "line2_angle",
                "valid_cue",
                "TP",
                "response",
                "participantID",
                "decision",
            ]
        ]

    # Load model decisions
    for cond in conds:
        base = data_dir / cond
        decisions_dir = base / "decisions_fixed"
        if not decisions_dir.exists():
            raise FileNotFoundError(
                f"decisions_fixed directory not found: {decisions_dir}. "
                "Data analysis should only use decisions_fixed folder."
            )

        for f in sorted(decisions_dir.glob("*.csv")):
            dfs.append(load_decisions(f, cond, f.stem))

        # Load Gemini angle-estimation model
        def parse_gemini(resp: str) -> tuple:
            a1, a2, dec = [p.strip() for p in str(resp).split(",")]
            return float(a1), float(a2), dec.lower()

        g = pd.read_csv(base / "angle_estimations" / "gemini-2.5-pro.csv")
        g[["est1", "est2", "response"]] = pd.DataFrame(
            g["GPT_response"].apply(parse_gemini).tolist(), index=g.index
        )
        g["stimID"] = g["image_id"]
        g["condition"] = cond
        g["participantID"] = "gemini-2.5-pro"
        g["decision"] = g["response"].map({"present": 1, "absent": 0})
        dfs.append(
            g[
                [
                    "stimID",
                    "condition",
                    "side_selected",
                    "cue_points",
                    "line1_angle",
                    "line2_angle",
                    "valid_cue",
                    "TP",
                    "response",
                    "participantID",
                    "decision",
                ]
            ]
        )

    model_df = pd.concat(dfs, ignore_index=True)

    # Filter bad model (0 responses)
    bad_model = "0responses_gemini-2.5-flash-lite-preview-06-17"
    model_df = model_df[model_df["participantID"] != bad_model]

    return model_df


# ============================================================================
# BIO (BAYESIAN IDEAL OBSERVER) DATA LOADER
# ============================================================================
def load_bio_master(data_dir: Path | None = None) -> pd.DataFrame:
    """Load and compute BIO (Bayesian Ideal Observer) metrics.

    Computes signal detection theory metrics (d', criterion, probability of
    signal present) for each trial based on angle estimation data.

    Returns:
        DataFrame with BIO metrics: stimID, condition, side_selected, cue_points,
        line1_angle, line2_angle, valid_cue, TP, participantID, bio_sigma,
        bio_lambda, bio_llr, bio_p_present, bio_decision, bio_outcome
    """
    if data_dir is None:
        paths = get_paths()
        data_dir = paths.data_dir

    conds = ["50_50", "80_20", "100_0"]
    bio_dfs = []

    for cond in conds:
        base = data_dir / cond
        g = pd.read_csv(base / "angle_estimations" / "gemini-2.5-pro.csv")

        g["stimID"] = g["image_id"]
        g["condition"] = cond
        g["participantID"] = "BIO"

        # Compute BIO metrics
        bio_metrics = compute_bio_metrics(g)
        g = pd.concat([g, bio_metrics], axis=1)

        # Binary decision from p_present
        g["bio_decision"] = (g["bio_p_present"] >= 0.5).astype(int)
        g["bio_outcome"] = (g["bio_decision"] == g["TP"]).astype(int)

        bio_dfs.append(
            g[
                [
                    "stimID",
                    "condition",
                    "side_selected",
                    "cue_points",
                    "line1_angle",
                    "line2_angle",
                    "valid_cue",
                    "TP",
                    "participantID",
                    "bio_sigma",
                    "bio_lambda",
                    "bio_llr",
                    "bio_p_present",
                    "bio_decision",
                    "bio_outcome",
                ]
            ]
        )

    return pd.concat(bio_dfs, ignore_index=True)


# ============================================================================
# HELPER: BIO METRIC COMPUTATION
# ============================================================================
def compute_bio_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Bayesian Ideal Observer metrics from angle data.

    Internal helper for load_bio_master().
    """
    # Angle difference from cue
    df_work = df.copy()
    df_work["angle_diff_cue"] = (
        df_work["line1_angle"] - df_work["line2_angle"]
    ) * df_work["cue_points"]
    df_work["angle_diff_noncue"] = (
        df_work["line1_angle"] - df_work["line2_angle"]
    ) * (1 - df_work["cue_points"])

    sigma = df_work["angle_diff_cue"].std()
    lambda_val = df_work["angle_diff_noncue"].std()

    results = []

    for _, row in df_work.iterrows():
        angle_diff = row["line1_angle"] - row["line2_angle"]

        if pd.isna(angle_diff):
            bio_sigma = np.nan
            bio_lambda = np.nan
            bio_llr = np.nan
            bio_p_present = np.nan
        else:
            bio_sigma = sigma if sigma > 0 else np.nan
            bio_lambda = lambda_val if lambda_val > 0 else np.nan
            bio_llr = (
                (angle_diff**2) / (2 * sigma**2) - (angle_diff**2) / (2 * lambda_val**2)
                if (sigma > 0 and lambda_val > 0)
                else np.nan
            )
            # Probability of signal present (prior 0.5)
            bio_p_present = 1 / (1 + np.exp(-bio_llr)) if np.isfinite(bio_llr) else np.nan

        results.append(
            {
                "bio_sigma": bio_sigma,
                "bio_lambda": bio_lambda,
                "bio_llr": bio_llr,
                "bio_p_present": bio_p_present,
            }
        )

    return pd.DataFrame(results)


__all__ = [
    "load_human_master",
    "load_model_master",
    "load_bio_master",
    "compute_bio_metrics",
]
