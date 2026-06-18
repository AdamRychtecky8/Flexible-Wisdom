"""Consolidated data loaders for human and model datasets.

Centralized functions to build master dataframes, avoiding duplication
across notebooks. All functions return properly formatted DataFrames
ready for analysis.

BIO (Bayesian Ideal Observer) is NOT loaded here; use src.bio.BayesianIdealObserver
directly in the Appendix-BIO-Analysis notebook.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

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

# Prefix applied to all CSV filenames in decisions_fixed/ — meaningless artifact.
_DECISIONS_PREFIX = "0responses_"


def _normalize_model_name(raw_stem: str) -> str:
    """Strip the decisions-file prefix and disambiguate duplicate gemini names.

    decisions_fixed/0responses_gemini-2.5-pro.csv  -> gemini-2.5-pro-decision
    angle_estimations/gemini-2.5-pro.csv           -> gemini-2.5-pro-angle
    (handled at call site for the angle file)
    """
    name = raw_stem
    if name.startswith(_DECISIONS_PREFIX):
        name = name[len(_DECISIONS_PREFIX):]
    # gemini-2.5-pro in decisions_fixed is the direct-decision variant
    if name == "gemini-2.5-pro":
        name = "gemini-2.5-pro-decision"
    return name


def load_model_master(data_dir: Path | None = None) -> pd.DataFrame:
    """Load and prepare model decision data across all conditions.

    Uses decisions_fixed/ directory only (plus the angle-estimation gemini variant).
    Filters the model with 0 valid responses. Strips the "0responses_" filename
    prefix from all model names; disambiguates the two gemini-2.5-pro variants as
    gemini-2.5-pro-decision (from decisions_fixed) and gemini-2.5-pro-angle (from
    angle_estimations).

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

    for cond in conds:
        base = data_dir / cond
        decisions_dir = base / "decisions_fixed"
        if not decisions_dir.exists():
            raise FileNotFoundError(
                f"decisions_fixed directory not found: {decisions_dir}. "
                "Data analysis should only use decisions_fixed folder."
            )

        for f in sorted(decisions_dir.glob("*.csv")):
            model_name = _normalize_model_name(f.stem)
            dfs.append(load_decisions(f, cond, model_name))

        # Load Gemini angle-estimation variant (decisions derived from angle estimates)
        def parse_gemini(resp: str) -> tuple:
            a1, a2, dec = [p.strip() for p in str(resp).split(",")]
            return float(a1), float(a2), dec.lower()

        g = pd.read_csv(base / "angle_estimations" / "gemini-2.5-pro.csv")
        g[["est1", "est2", "response"]] = pd.DataFrame(
            g["GPT_response"].apply(parse_gemini).tolist(), index=g.index
        )
        g["stimID"] = g["image_id"]
        g["condition"] = cond
        g["participantID"] = "gemini-2.5-pro-angle"
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

    # Exclude the model that returned 0 valid responses
    bad_model = "gemini-2.5-flash-lite-preview-06-17"
    model_df = model_df[model_df["participantID"] != bad_model]

    return model_df


__all__ = [
    "load_human_master",
    "load_model_master",
]
