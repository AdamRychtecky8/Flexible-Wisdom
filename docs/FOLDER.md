# Workspace Folder Structure

Complete reference for the Flexible-Wisdom project layout. See [QUICKSTART.md](QUICKSTART.md) for how to run the pipeline.

---

## Directory Tree

```
Flexible-Wisdom/
├── docs/                               # Documentation (this folder)
│   ├── QUICKSTART.md                  # How to run the pipeline ← START HERE
│   ├── FOLDER.md                      # This file (workspace reference)
│   ├── FUTURE_DIRECTIONS.md           # Research trajectory & north star
│   ├── NEXT_IDEAS.md                  # Strategic guide for LLM research
│   ├── PROJECT_OVERVIEW.md            # Research goals & task description
│   ├── WORKLOG.md                     # Session notes & progress
│   └── README.md                      # (not present, but documented)
│
├── src/                                # Core Python modules (non-notebook code)
│   ├── config.py                      # Path management & .env parsing (71 lines)
│   ├── data_loaders.py                # Data loading functions (human, model, BIO) (283 lines)
│   ├── data_registration.py           # Legacy/auxiliary code
│   └── __pycache__/                   # Python bytecode (auto-generated)
│
├── notebooks/                          # Active analysis pipeline (run in order ↓)
│   ├── Data-Preparation.ipynb         # [1] Load & validate all datasets (~2 min)
│   ├── Main-Analysis.ipynb            # [2] Majority voting, WLC, SDT metrics (~5 min)
│   ├── Individual-Differences.ipynb   # [3] Per-participant/model analysis (~2 min)
│   ├── Model-Comparison.ipynb         # [4] Model agreement & error patterns (~2 min)
│   ├── Appendix-BIO-Analysis.ipynb    # [5] Bayesian Ideal Observer (optional, ~2 min)
│   ├── Mod-Hum-Comparison.ipynb       # Legacy notebook (inactive, kept for reference)
│   ├── README.md                      # Notebook execution guide & order
│   ├── _utils.py                      # Helper functions (deprecated; use src/data_loaders instead)
│   ├── notebooks_text/                # Exported .py versions of notebooks (generated)
│   │   └── Mod-Hum-Comparison.py      # Jupytext export
│   └── __pycache__/                   # Python bytecode (auto-generated)
│
├── reports/                            # Analysis reports & publications
│   ├── README.md                      # Report navigation guide
│   ├── Report-Baseline-Analysis.ipynb # Interactive baseline analysis notebook
│   └── REPORT-BASELINE-ANALYSIS.md    # Publication-ready baseline report (~10 pages)
│
├── data/                               # Input data (git-ignored, private)
│   ├── raw/                           # Main data folder (set via .env DATA_DIR)
│   │   ├── 50_50/                     # 50% cue validity (hard condition)
│   │   │   ├── human_data.csv         # 13,000 human trials
│   │   │   ├── decisions_fixed/       # Model decision files (REQUIRED for analysis)
│   │   │   │   ├── gemini-2.5-flash-lite-preview-06-17.csv
│   │   │   │   ├── gpt-4o.csv
│   │   │   │   ├── claude-3-5-sonnet.csv
│   │   │   │   └── ... (12+ model files)
│   │   │   ├── decisions/             # Legacy (unused - DO NOT USE)
│   │   │   └── angle_estimations/     # Model angle responses (supplementary)
│   │   │       ├── gemini-2.5-pro.csv
│   │   │       ├── gpt-4o.csv
│   │   │       └── ... (12+ model files)
│   │   ├── 80_20/                     # 80% cue validity (medium condition)
│   │   │   └── (same structure as 50_50)
│   │   └── 100_0/                     # 100% cue validity (easy condition)
│   │       └── (same structure as 50_50)
│   ├── data.zip                       # Backup of data archive (optional)
│   └── README.md                      # Data folder documentation
│
├── outputs/                            # Results (git-ignored, auto-generated)
│   ├── majority-voting-bootstrap.csv         # 500 bootstrap results (18k rows)
│   ├── wlc-cv-results.csv                    # WLC cross-validation results
│   ├── individual-differences.csv            # Per-participant/model metrics
│   ├── model-agreement-matrix.csv            # Pairwise model agreement
│   ├── model-error-correlation.csv           # Error correlation patterns
│   ├── model-condition-performance.csv       # Performance by condition
│   ├── report-individual-distributions.pdf  # Performance histograms
│   ├── report-group-size-effects.pdf         # Ensemble size effects
│   └── ... (additional plots & CSVs generated during analysis)
│
├── archive/                            # Old results (preserved for reference)
│   └── (previous analysis outputs; cleared before new runs)
│
├── exports/                            # Archived notebooks (exploratory, superseded)
│   ├── Gemini_exploration.ipynb        # Old model validation (archived)
│   ├── Human_exploration.ipynb         # Old per-participant analysis (archived)
│   └── Model_exploration.ipynb         # Old model breakdowns (archived)
│
├── .vscode/                            # VS Code workspace settings (git-tracked)
│   └── settings.json
│
├── .env                                # Local config: DATA_DIR path (git-ignored)
├── .env.example                        # Template for .env (committed)
├── .gitignore                          # Excludes: data/, outputs/, archive/, .env, etc.
├── .gitattributes                      # Git line ending config
├── environment.yml                     # Conda environment spec (Python + packages)
├── README.md                           # Project overview (repo root)
├── NOTEBOOK-REFACTOR-SUMMARY.md        # Detailed refactoring notes & decisions
└── data.zip                            # Backup/archive of data (optional)

```

---

## Key Files & Directories

### 🚀 Documentation (START HERE)

| File | Purpose | Read Time | Priority |
|------|---------|-----------|----------|
| **`docs/QUICKSTART.md`** | Setup & execution guide | 7 pages | ⭐⭐⭐ Must read first |
| **`docs/FOLDER.md`** | This file; workspace reference | 5 pages | Reference |
| **`docs/PROJECT_OVERVIEW.md`** | Research context & task description | 3 pages | ⭐⭐ Background |
| **`docs/FUTURE_DIRECTIONS.md`** | Research options & correlation blindness rationale | 4 pages | ⭐⭐ Strategic planning |
| **`docs/NEXT_IDEAS.md`** | LLM study protocol: tiered prompting methodology | 6 pages | ⭐ Future research |
| **`docs/WORKLOG.md`** | Session notes & progress tracking | Variable | Reference |

### 📊 Reports & Analysis

| File | Purpose | Status | Audience |
|------|---------|--------|----------|
| **`reports/Report-Baseline-Analysis.ipynb`** | Interactive baseline analysis (10 sections, 39.6k trials) | ✅ Complete | Interactive exploration |
| **`reports/REPORT-BASELINE-ANALYSIS.md`** | Publication-ready baseline report (10 pages) | ✅ Complete | ⭐ Advisor review |
| **`NOTEBOOK-REFACTOR-SUMMARY.md`** | Detailed refactoring decisions & progress notes | ✅ Complete | Technical reference |

### ⚙️ Configuration & Setup

| File | Purpose | Details |
|------|---------|---------|
| **`.env`** | Local config (git-ignored) | Set `DATA_DIR=/path/to/data/raw` here; create from `.env.example` |
| **`.env.example`** | Config template (committed) | Reference for all `.env` settings; platform-agnostic examples |
| **`environment.yml`** | Conda environment | `conda env create -f environment.yml` to set up Python + packages |

### 📦 Core Modules

| File | Purpose | Key Functions |
|------|---------|---|
| **`src/config.py`** | Path management & .env parsing | `load_env(env_path)` – reads .env file; `get_paths()` – validates DATA_DIR, returns ProjectPaths |
| **`src/data_loaders.py`** | Centralized data access (283 lines) | `load_human_master()` – 39.6k trials; `load_model_master()` – 468k+ trials; `load_bio_master()` – BIO metrics |
| **`src/data_registration.py`** | Legacy code | Auxiliary functions (rarely used) |

**Important:** 
- All notebooks import from `src/data_loaders` (single source of truth)
- No hardcoded paths; all use `src/config.get_paths()`
- Data loading is cached; kernel restart required after data file changes

---

### 📓 Analysis Notebooks (Active Pipeline)

**Execution Order: CRITICAL ⚠️**

| Order | Notebook | Runtime | Purpose | Output |
|-------|----------|---------|---------|--------|
| **1** | **Data-Preparation.ipynb** | ~2 min | Load & validate all datasets (human, model, BIO) | Validation summary (prints only) |
| **2** | **Main-Analysis.ipynb** | ~5 min | Core results: majority voting bootstrap, WLC, SDT metrics | 6 CSVs + 3 PDFs |
| **3** | **Individual-Differences.ipynb** | ~2 min | Per-participant/model performance, heatmaps, outliers | 1 CSV + 2 PDFs |
| **4** | **Model-Comparison.ipynb** | ~2 min | Model agreement, diversity, error correlation | 2 CSVs + 2 PDFs |
| **5** | **Appendix-BIO-Analysis.ipynb** | ~2 min | Bayesian Ideal Observer (theoretical benchmark, optional) | Exploratory plots |

**Prerequisites:**
```
✅ Data-Preparation must run first (validates data integrity)
✅ All subsequent notebooks use cached data from step 1
⚠️ Do NOT skip Data-Preparation
⚠️ Always run Appendix-BIO last (it's optional)
```

**Notebook Details:**
- **Mod-Hum-Comparison.ipynb** – Legacy notebook (inactive, kept for reference)
- **notebooks/README.md** – Execution guide & troubleshooting
- **notebooks/_utils.py** – Helper functions (deprecated; use `src/data_loaders` instead)
- **notebooks/notebooks_text/** – Auto-generated .py exports (Jupytext)

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
