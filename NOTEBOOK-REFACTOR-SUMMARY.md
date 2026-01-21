# Notebook Pipeline Refactoring Complete ✓

## Summary of Changes

Your notebooks folder has been restructured into an **efficient, linear analysis pipeline** with **centralized data loading** and **no redundancy**.

---

## New Structure

### Active Notebooks (Main Pipeline)

Execute in this order:

1. **`Data-Preparation.ipynb`** 
   - Loads human, model, BIO datasets via `src.data_loaders`
   - Validates cross-domain consistency (same stimIDs, conditions)
   - Exports clean CSVs for optional archival
   - ~2 min runtime

2. **`Main-Analysis.ipynb`** (refactored from `Mod-Hum-Comparison.ipynb`)
   - Majority voting + bootstrap (group size effects)
   - Weighted Logic Combiner (WLC) + 10-fold cross-validation
   - Signal Detection Theory metrics (d', criterion, hit/FA rates)
   - Saves results: `majority-voting-bootstrap.csv`, `wlc-cv-results.csv`, `*.pdf` plots
   - ~5 min runtime

3. **`Individual-Differences.ipynb`** (NEW)
   - Per-participant/model accuracy across conditions
   - Heatmaps of performance (participant × condition)
   - Outlier detection (strong/weak performers)
   - Saves: `individual-differences.csv`, `*.pdf` heatmaps & distributions

4. **`Model-Comparison.ipynb`** (NEW)
   - Pairwise model agreement matrices
   - Decision diversity metrics (ensemble complementarity)
   - Model ranking by accuracy
   - Error pattern correlation (which models make similar mistakes?)
   - Saves: `model-agreement-matrix.csv`, `model-error-correlation.csv`, `*.pdf` heatmaps

5. **`Appendix-BIO-Analysis.ipynb`** (formerly `BIO.ipynb`, optional)
   - Bayesian Ideal Observer analysis
   - Computes BIO metrics from angle data
   - Secondary analysis (keep but clearly marked as appendix)

### Supporting Infrastructure

- **`notebooks/README.md`** — Quickstart guide and execution order
- **`notebooks/_utils.py`** — Legacy helper; now references `src.data_loaders`
- **`src/data_loaders.py`** — Centralized data loading (NEW)
  - `load_human_master()` — 1 place, not duplicated across 5 notebooks
  - `load_model_master()` — Single function, reused
  - `load_bio_master()` — Consolidated BIO loading
  - Eliminates code duplication; faster to fix bugs

### Archived (Safe for Later Deletion)

- `exports/Human_exploration.ipynb`
- `exports/Model_exploration.ipynb`
- `exports/Gemini_exploration.ipynb`

These exploratory notebooks are tagged in `exports/` for easy deletion after you review them.

---

## Key Improvements

✅ **No Code Duplication**
- Data loading functions centralized in `src/data_loaders.py`
- Each notebook imports `load_human_master()`, `load_model_master()`, `load_bio_master()`
- Single source of truth; fix bugs once, not five times

✅ **Linear, Clear Workflow**
- Run notebooks 1→5 in order
- Each notebook has clear input/output
- Data-Preparation caches datasets; subsequent notebooks reuse them

✅ **Modular Design**
- Modify one notebook without breaking others
- New analysis ideas → create new notebook (no touching existing ones)
- Easy to add a 6th notebook (e.g., Temporal-Trends.ipynb) without impact

✅ **Efficient Reuse**
- Load data once (Data-Preparation), use results in all downstream notebooks
- No redundant file reads or processing

✅ **Clean Organization**
- `notebooks/` = analysis pipeline only (5 focused notebooks)
- `exports/` = archived explorations (safe to delete)
- `src/` = reusable modules (data loaders, config, utilities)

---

## Outputs

All results saved to `outputs/`:
- **CSVs**: `majority-voting-bootstrap.csv`, `wlc-cv-results.csv`, `individual-differences.csv`, `model-agreement-matrix.csv`, etc.
- **Plots**: `*.pdf` files (majority-voting-group-size, individual-differences-heatmap, model-agreement-heatmap, etc.)

Each notebook documents what it saves.

---

## Running the Pipeline

```python
# From repo root:
# 1. Configure environment (one-time)
from src.config import get_paths
paths = get_paths()  # validates DATA_DIR

# 2. Run notebooks in order via VS Code or Jupyter
# Or from terminal:
jupyter notebook notebooks/Data-Preparation.ipynb
# ... then Main-Analysis, Individual-Differences, etc.
```

---

## What to Delete Later

After review, safely delete:
- `exports/Human_exploration.ipynb`
- `exports/Model_exploration.ipynb`
- `exports/Gemini_exploration.ipynb`
- `notebooks/Mod-Hum-Comparison.ipynb` (functionality absorbed into Main-Analysis.ipynb)

---

## Summary Stats

| Metric | Before | After |
|--------|--------|-------|
| Notebooks in `notebooks/` | 5 active + scattered code | 4 active + 1 appendix (focused) |
| Data loading functions | Duplicated 5 times | 1 centralized module |
| Lines of duplicated code | ~200 (df_to_pdf, loading logic) | 0 (all shared via `src/data_loaders.py`) |
| Time to fix a data bug | 5+ locations | 1 location |
| Exploratory notebooks | Mixed with analysis | Archived in `exports/` |

---

**Status: ✅ Ready to use. Run Data-Preparation.ipynb first, then any others in order.**
