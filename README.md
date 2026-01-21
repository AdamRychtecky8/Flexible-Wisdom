# Flexible Collective Wisdom

Undergrad research project in the UCSB Vision & Image Understanding Lab. Replicating & extending Juni & Eckstein (2015) to compare human collective adaptation with LLM ensembles.

## Quick Start

1. **Setup data access:**
   - Copy `.env.example` to `.env` and set `DATA_DIR` to your local data path (e.g., `data/raw`)
   - Data should be organized as: `DATA_DIR/{50_50, 80_20, 100_0}/human_data.csv` and model decisions

2. **Run main analysis:**
   - Notebooks in `notebooks/` contain the analysis pipeline
   - Start with `Mod-Hum-Comparison.ipynb` for the full human-vs-model comparison

3. **Project structure:**
   ```
   ├── data/raw/              # Raw dataset (git-ignored, local only)
   ├── src/                   # Core modules (config, data loaders)
   ├── notebooks/             # Analysis notebooks (.ipynb)
   ├── exports/               # Jupytext exports of notebooks (read-only)
   ├── outputs/               # Latest run results (metrics, plots)
   ├── archive/               # Old results and experiments
   └── docs/                  # Project documentation
   ```

## Key Modules

- `src/config.py` — Data path resolution & project paths
- `notebooks/_utils.py` — Shared notebook utilities (loaders, plotters)

## Constraints & Scope

- Budget: $700 for model API calls
- Timeline: 5 months
- Keep lightweight; avoid complex infrastructure
