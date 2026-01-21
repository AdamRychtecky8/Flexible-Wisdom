# Analysis Notebooks

This folder contains the analysis pipeline for comparing human and LLM collective decision-making.

## Quick Start

Run notebooks in this order:

1. **`Data-Preparation.ipynb`** — Load & validate all datasets
   - Builds master dataframes (human, model, BIO)
   - Data quality checks
   - ~2 min to run

2. **`Main-Analysis.ipynb`** — Core analysis
   - Majority voting bootstrap (group size effects)
   - Weighted Logic Combiner (WLC) with cross-validation
   - Signal Detection Theory metrics
   - ~5 min to run

3. **`Individual-Differences.ipynb`** — Per-participant breakdown
   - Individual accuracy across conditions
   - Performance heterogeneity
   - Outlier detection
   - ~2 min to run

4. **`Model-Comparison.ipynb`** — Ensemble analysis
   - Pairwise model agreement
   - Decision diversity metrics
   - Model ranking & complementarity
   - ~2 min to run

5. **`Appendix-BIO-Analysis.ipynb`** — (Optional) Bayesian Ideal Observer
   - Computes BIO predictions
   - Compares against human/model
   - Specialized analysis

---

## Directory Structure

```
notebooks/
├── _utils.py                         # Shared utilities
├── Data-Preparation.ipynb            # 1. Data loading & validation
├── Main-Analysis.ipynb               # 2. Core analysis (majority voting + WLC)
├── Individual-Differences.ipynb      # 3. Per-participant performance
├── Model-Comparison.ipynb            # 4. Model ensemble analysis
├── Appendix-BIO-Analysis.ipynb       # (Optional) BIO analysis
└── notebooks_text/                   # (Ignored) Jupytext exports
```

---

## Key Modules

- **`src/config.py`** — Data path management (`get_paths()`)
- **`src/data_loaders.py`** — Consolidated data loading functions:
  - `load_human_master()` — Human participant data
  - `load_model_master()` — LLM decisions
  - `load_bio_master()` — Bayesian Ideal Observer

---

## Output Files

All results saved to `outputs/`:
- `*.csv` — Data tables (bootstrap results, individual metrics, etc.)
- `*.pdf` — Publication-quality plots (group size effects, heatmaps, etc.)

---

## Archived Notebooks

Old exploratory notebooks are in `exports/` for reference:
- `Human_exploration.ipynb`
- `Model_exploration.ipynb`
- `Gemini_exploration.ipynb`

These can be safely deleted after review.
