# Workspace Folder Structure

Complete reference for the Flexible-Wisdom project layout. See [QUICKSTART.md](QUICKSTART.md) for how to run the pipeline.

---

## Directory Tree

```
Flexible-Wisdom/
├── docs/                           # Documentation (this folder)
│   ├── QUICKSTART.md              # How to run the pipeline ← START HERE
│   ├── FOLDER.md                  # This file (workspace reference)
│   ├── PROJECT_OVERVIEW.md        # Research goals & constraints
│   └── WORKLOG.md                 # Session notes & progress
│
├── src/                            # Core Python modules (non-notebook code)
│   ├── config.py                  # Path management & .env parsing
│   ├── data_loaders.py            # Data loading functions (human, model, BIO)
│   └── data_registration.py       # Legacy/auxiliary code
│
├── notebooks/                      # Active analysis pipeline (run in order ↓)
│   ├── Data-Preparation.ipynb     # [1] Load & validate all datasets
│   ├── Main-Analysis.ipynb        # [2] Majority voting, WLC, SDT metrics
│   ├── Individual-Differences.ipynb # [3] Per-participant/model analysis
│   ├── Model-Comparison.ipynb     # [4] Model agreement & error patterns
│   ├── Appendix-BIO-Analysis.ipynb # [5] Bayesian Ideal Observer (optional)
│   ├── Mod-Hum-Comparison.ipynb   # [ARCHIVED] Legacy notebook
│   ├── README.md                  # Notebook execution guide
│   ├── _utils.py                  # Legacy helpers (deprecated)
│   ├── notebooks_text/            # Exported .py versions of notebooks
│   │   └── Mod-Hum-Comparison.py
│   └── __pycache__/               # Python bytecode (auto-generated)
│
├── data/                           # Input data (git-ignored, private)
│   ├── raw/                       # Main data folder (set via .env DATA_DIR)
│   │   ├── 50_50/                 # 50% signal condition
│   │   │   ├── human_data.csv     # 13,000 human trials
│   │   │   ├── decisions_fixed/   # Model decision files
│   │   │   │   ├── gemini-2.5-flash-lite-preview-06-17.csv
│   │   │   │   ├── gpt-4o.csv
│   │   │   │   └── ... (12+ models)
│   │   │   └── angle_estimations/ # Model angle responses
│   │   │       ├── gemini-2.5-pro.csv
│   │   │       ├── gpt-4o.csv
│   │   │       └── ... (12+ models)
│   │   ├── 80_20/                 # 80% signal condition (same structure)
│   │   └── 100_0/                 # 100% signal condition (same structure)
│   └── README.md                  # Data folder info
│
├── outputs/                        # Results (git-ignored, auto-generated)
│   ├── majority-voting-bootstrap.csv       # 500 bootstrap results
│   ├── wlc-cv-results.csv                  # WLC cross-validation
│   ├── individual-differences.csv          # Per-participant metrics
│   ├── model-agreement-matrix.csv          # Model pairwise agreement
│   ├── model-error-correlation.csv         # Model error similarity
│   ├── model-condition-performance.csv     # Accuracy by model & condition
│   ├── *.pdf                               # Visualization plots
│   └── ...
│
├── archive/                        # Old results (git-ignored)
│   ├── human_majority_summary.csv
│   ├── human_majority_bootstrap_results.csv
│   ├── human_model_majority_summary.csv
│   ├── human_model_majority_bootstrap_results.csv
│   └── ... (previous analysis outputs)
│
├── exports/                        # Archived notebooks (exploratory, superseded)
│   ├── Gemini_exploration.ipynb    # Old model validation
│   ├── Human_exploration.ipynb     # Old per-participant analysis
│   └── Model_exploration.ipynb     # Old model breakdowns
│
├── reports/                        # Report outputs (git-ignored, optional)
│   └── (auto-generated reports)
│
├── .env                            # Local config: DATA_DIR path (git-ignored)
├── .env.example                    # Template for .env (committed)
├── .gitignore                      # Excludes: data/, outputs/, archive/, exports/, .env
├── environment.yml                 # Conda dependencies & Python version
├── README.md                       # Project overview (repo root)
└── NOTEBOOK-REFACTOR-SUMMARY.md   # Detailed refactoring notes

```

---

## Key Files & Directories

### 🚀 Configuration & Setup

| File | Purpose | Details |
|------|---------|---------|
| **`.env`** | Local config (git-ignored) | Set `DATA_DIR=/path/to/data/raw` here; create from `.env.example` |
| **`.env.example`** | Config template (committed) | Reference for all `.env` settings; platform-agnostic examples |
| **`environment.yml`** | Conda environment | `conda env create -f environment.yml` to set up Python + packages |

---

### 📊 Data Modules

| File | Purpose | Key Functions |
|------|---------|---|
| **`src/config.py`** | Path management | `load_env(env_path)` – reads .env file; `get_paths()` – validates DATA_DIR, returns ProjectPaths |
| **`src/data_loaders.py`** | Data access (centralized) | `load_human_master()` – loads 39k human trials; `load_model_master()` – loads 12+ models; `load_bio_master()` – computes BIO metrics |
| **`src/data_registration.py`** | Legacy code | Auxiliary functions (rarely used) |

**Important:** 
- All notebooks use `src/data_loaders` to load data
- No hardcoded paths; all use `src/config.get_paths()`
- Data loading is cached; changes to `.csv` files require notebook kernel restart

---

### 📓 Analysis Notebooks (Active Pipeline)

| Notebook | Runtime | Purpose | Prerequisite | Output |
|----------|---------|---------|---|---|
| **Data-Preparation.ipynb** | ~2 min | Load & validate all datasets (human, model, BIO) | None | Prints summary; no CSV |
| **Main-Analysis.ipynb** | ~5 min | Core results: majority voting bootstrap, WLC, SDT metrics | Data-Prep | 6 CSVs + 3 PDFs |
| **Individual-Differences.ipynb** | ~2 min | Per-participant/model performance, heatmaps, outliers | Data-Prep | 1 CSV + 2 PDFs |
| **Model-Comparison.ipynb** | ~2 min | Model agreement, diversity, error correlation | Data-Prep | 2 CSVs + 2 PDFs |
| **Appendix-BIO-Analysis.ipynb** | ~2 min | Bayesian Ideal Observer (theoretical benchmark) | Data-Prep | Optional; exploratory |

**Execution Order:** CRITICAL ⚠️
```
1. Data-Preparation  (loads all data)
2. Main-Analysis     (reuses cached data)
3. Individual-Differences
4. Model-Comparison
5. Appendix-BIO-Analysis (optional)
```

⚠️ **Always run Data-Preparation first!** It validates datasets that other notebooks depend on.

---

### 🗂️ Data Organization

**Location:** `data/raw/` (set via `.env` → `DATA_DIR`)

**Structure:**
```
data/raw/
├── 50_50/          # 50% signal strength (difficulty: hard)
├── 80_20/          # 80% signal strength (difficulty: medium)
└── 100_0/          # 100% signal strength (difficulty: easy)
```

**Each condition folder contains:**
```
{condition}/
├── human_data.csv                      # 13,000 human trials
│   Columns: trial_id, participant_id, condition, signal, stim_id,
│   response, confidence, decision (binary), ...
│
├── decisions_fixed/                    # Model binary decisions (preferred)
│   ├── gemini-2.5-pro.csv             # 13,000 trials × 2 cols
│   ├── gpt-4o.csv
│   └── ... (12+ model decision files)
│
└── angle_estimations/                  # Model angle responses (supplementary)
    ├── gemini-2.5-pro.csv             # Continuous angle estimates
    ├── gpt-4o.csv
    └── ...
```

**Data Characteristics:**
- **Human Data:** 12 participants × 3 conditions × ~1,100 trials = 39,600 total trials
- **Model Data:** 12+ models × 3 conditions × 13,000 trials = 468,000+ total trials
- **BIO (Bayesian Ideal Observer):** Theoretical optimal performance; computed in pipeline

---

### 📁 Results & Archives

| Folder | Purpose | Git Status | Notes |
|--------|---------|-----------|-------|
| **`outputs/`** | Active results | Git-ignored | Latest CSVs & PDFs; cleared before new runs |
| **`archive/`** | Old results | Git-ignored | Previous analysis outputs; preserved for reference |
| **`exports/`** | Archived notebooks | Git-ignored | Exploratory notebooks (Human_, Model_, Gemini_exploration.ipynb) |
| **`reports/`** | Report outputs | Git-ignored | Optional; for final report generation |

**Naming Conventions:**
- CSVs: `{analysis-name}-{condition|metric}-results.csv`
- PDFs: `{analysis-name}-{plot-type}.pdf`
- Timestamps: Appended only if multiple runs same day (e.g., `majority-voting-bootstrap_20240601_1.csv`)

---

### 📖 Documentation

| File | Purpose | Audience |
|------|---------|----------|
| **`docs/QUICKSTART.md`** | How to run the pipeline | Users / newbies |
| **`docs/FOLDER.md`** | This file; workspace reference | Developers / explorers |
| **`docs/PROJECT_OVERVIEW.md`** | Research goals & data constraints | Researchers / context |
| **`docs/WORKLOG.md`** | Session notes & decisions | Project historians |
| **`notebooks/README.md`** | Notebook execution guide | Notebook users |

---

### 🔧 Configuration Files

| File | Purpose | Edit? |
|------|---------|-------|
| **`.gitignore`** | Git exclusions | ✗ Do not edit; data/, outputs/, .env already excluded |
| **`environment.yml`** | Conda spec | ✓ Edit to add packages; then `conda env update` |
| **`NOTEBOOK-REFACTOR-SUMMARY.md`** | Refactoring notes | ✗ Reference only; details notebook consolidation |

---

## Workflow Reference

### New Analysis Session

```bash
# 1. Activate environment
conda activate flexwisdom

# 2. Verify setup
python -c "from src.config import get_paths; get_paths()"

# 3. Run notebooks in order
# Open: notebooks/Data-Preparation.ipynb → Run All
# Open: notebooks/Main-Analysis.ipynb → Run All
# ... (continue with other notebooks)

# 4. Check outputs
ls outputs/*.csv    # New CSVs generated
ls outputs/*.pdf    # New plots generated

# 5. Git commit if ready
git add outputs/
git commit -m "analysis: run full pipeline with updated models"
```

### Adding a New Model

```bash
# 1. Save model decision file to:
# data/raw/{condition}/decisions_fixed/{model-name}.csv

# 2. Rerun Data-Preparation → Main-Analysis
# (src/data_loaders automatically picks up new files)

# 3. New model results appear in outputs/
```

### Modifying Data Loading

```bash
# 1. Edit: src/data_loaders.py
# 2. All notebooks auto-reload from that module
# 3. No need to edit individual notebooks
```

---

## Size Reference

| Component | Size | Notes |
|-----------|------|-------|
| `data/raw/` | ~2-4 GB | Contains all 39,600+ trials across conditions & models |
| `notebooks/` | ~5 MB | Jupyter notebooks (text-based) |
| `outputs/` | ~50-100 MB | Generated CSVs + PDFs per analysis run |
| `archive/` | ~50-100 MB | Previous results; can be deleted to save space |
| `exports/` | ~5 MB | Archived exploratory notebooks |
| **Total (with data)** | **~2.5-4.5 GB** | Mostly data; code + outputs ~100 MB |

---

## Getting Help

| Question | Resource |
|----------|----------|
| "How do I run the pipeline?" | → [QUICKSTART.md](QUICKSTART.md) |
| "What is this analysis doing?" | → Notebook markdown cells & code comments |
| "Why did we refactor notebooks?" | → NOTEBOOK-REFACTOR-SUMMARY.md |
| "What are the research goals?" | → [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) |
| "How do I set up the data?" | → [QUICKSTART.md § 2: Data Organization](QUICKSTART.md#2-data-organization) |
| "Where do results go?" | → `outputs/` folder or [§ Results & Archives](#-results--archives) above |

---

**Last Updated:** Message 20 (Documentation Phase)  
**Git Branch:** `migration`  
**Status:** ✅ Complete & ready for analysis
