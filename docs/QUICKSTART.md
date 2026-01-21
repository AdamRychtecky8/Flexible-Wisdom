# Quickstart: Running the Analysis Pipeline

Complete walkthrough to set up and run the full analysis from start to finish.

---

## 1. Environment Setup (One-Time)

### Step 1a: Create Conda Environment
```bash
cd c:\Users\AdamR\Projects\Flexible-Wisdom
conda env create -f environment.yml
conda activate flexwisdom
```

### Step 1b: Configure Data Access
```bash
# Copy the template
copy .env.example .env

# Edit .env and set DATA_DIR to your local data path
# For example:
# DATA_DIR=C:\Users\AdamR\Projects\Flexible-Wisdom\data\raw
```

**Verify setup:**
```python
from src.config import get_paths
paths = get_paths()
print(f"✓ Data: {paths.data_dir}")
print(f"✓ Outputs: {paths.outputs_dir}")
```

---

## 2. Data Organization

Ensure your data folder structure is:
```
data/raw/
├── 50_50/
│   ├── human_data.csv
│   ├── decisions_fixed/
│   │   └── *.csv (model decisions)
│   └── angle_estimations/
│       └── gemini-2.5-pro.csv
├── 80_20/
│   └── (same structure)
└── 100_0/
    └── (same structure)
```

Run the data access test to verify:
```bash
# From repo root:
python -c "from src.config import get_paths; paths = get_paths(); print(f'✓ DATA_DIR: {paths.data_dir}')"
```

---

## 3. Run Analysis Pipeline

### Order: CRITICAL ⚠️

**Always run notebooks in this exact order:**

#### **Step 1: Data Preparation** (~2 min)
```
Open: notebooks/Data-Preparation.ipynb
Purpose: Load & validate all datasets
Output: Prints summary statistics; no CSV output (data cached in memory)
Action: Run all cells (Ctrl+Alt+Enter or ▶ Run All)
```

**Check output:**
- ✓ Human: 39,000 trials, 12 participants
- ✓ Model: 39,000 trials, 12+ models  
- ✓ BIO: 39,000 trials (Bayesian Ideal Observer)

---

#### **Step 2: Main Analysis** (~5 min)
```
Open: notebooks/Main-Analysis.ipynb
Purpose: Core comparisons (majority voting, WLC, SDT metrics)
Prerequisites: Run Data-Preparation.ipynb first
Output: 
  - majority-voting-bootstrap.csv
  - wlc-cv-results.csv
  - *.pdf plots (group size effects, WLC performance)
Action: Run all cells
```

**Key Results:**
- Group size effects: Does accuracy improve with larger voting groups?
- WLC performance: Can weighted combination beat majority voting?
- SDT metrics: d' (discriminability), criterion (response bias)

---

#### **Step 3: Individual Differences** (~2 min)
```
Open: notebooks/Individual-Differences.ipynb
Purpose: Per-participant/model performance breakdown
Prerequisites: Run Data-Preparation.ipynb first
Output:
  - individual-differences.csv
  - *.pdf heatmaps (participant × condition)
  - accuracy distribution plots
Action: Run all cells
```

**Insights:**
- Which participants/models are strongest/weakest?
- How does performance vary by condition (50_50, 80_20, 100_0)?
- Outlier detection: unusual performers

---

#### **Step 4: Model Comparison** (~2 min)
```
Open: notebooks/Model-Comparison.ipynb
Purpose: Understand model ensemble composition
Prerequisites: Run Data-Preparation.ipynb first
Output:
  - model-agreement-matrix.csv
  - model-error-correlation.csv
  - *.pdf heatmaps (agreement, error patterns)
Action: Run all cells
```

**Insights:**
- Which models make similar decisions? (redundancy)
- Which models are complementary? (diversity)
- Model ranking by accuracy
- Error pattern correlation (do similar models make similar mistakes?)

---

#### **Step 5 (Optional): Appendix BIO Analysis** (~2 min)
```
Open: notebooks/Appendix-BIO-Analysis.ipynb
Purpose: Bayesian Ideal Observer (theoretical benchmark)
Prerequisites: Run Data-Preparation.ipynb first
Output: BIO performance metrics, comparison to human/model
Action: Run all cells (optional; secondary analysis)
```

---

## 4. Review Results

### Output Files Location
All results saved to: `outputs/`

**CSVs:**
```
outputs/
├── majority-voting-bootstrap.csv       # 500 bootstraps × groups × domains
├── wlc-cv-results.csv                  # 10-fold CV results
├── individual-differences.csv          # Per-participant metrics
├── model-agreement-matrix.csv          # Pairwise model agreement
├── model-error-correlation.csv         # Error pattern correlations
└── model-condition-performance.csv     # Model accuracy by condition
```

**PDFs:**
```
outputs/
├── majority-voting-group-size.pdf      # Group size effect plots
├── individual-differences-heatmap.pdf  # Participant performance matrix
├── accuracy-distribution.pdf           # Histogram of accuracies
├── dprime-by-condition.pdf             # Signal detectability
├── model-agreement-heatmap.pdf         # Model agreement matrix
├── model-accuracy-ranking.pdf          # Model performance bars
└── model-error-correlation.pdf         # Error pattern similarity
```

---

## 5. Full Pipeline Script (Optional)

Run all notebooks at once from terminal:
```python
import subprocess
from pathlib import Path

notebooks = [
    "Data-Preparation.ipynb",
    "Main-Analysis.ipynb",
    "Individual-Differences.ipynb",
    "Model-Comparison.ipynb",
]

for nb in notebooks:
    print(f"\n{'='*60}")
    print(f"Running: {nb}")
    print('='*60)
    subprocess.run([
        "jupyter", "nbconvert",
        f"notebooks/{nb}",
        "--to", "notebook",
        "--inplace",
        "--execute",
        "--ExecutePreprocessor.timeout=600"
    ])
    print(f"✓ {nb} complete")
```

---

## 6. Troubleshooting

### Issue: "DATA_DIR not set"
**Solution:** 
1. Check `.env` exists in repo root
2. Verify `DATA_DIR=C:\path\to\data` is set correctly
3. Path must exist: `Path(DATA_DIR).exists()` should return `True`

### Issue: "ModuleNotFoundError: src"
**Solution:** 
1. Run notebooks from repo root, not a subdirectory
2. Or add to notebook cell 1: `import sys; sys.path.insert(0, '/path/to/Flexible-Wisdom')`

### Issue: "FileNotFoundError: angle_estimations/gemini-2.5-pro.csv"
**Solution:** Verify data structure matches:
```
data/raw/50_50/angle_estimations/gemini-2.5-pro.csv  ✓
data/raw/80_20/angle_estimations/gemini-2.5-pro.csv  ✓
data/raw/100_0/angle_estimations/gemini-2.5-pro.csv  ✓
```

### Issue: Notebooks run slowly
**Solution:** 
- Data-Preparation caches datasets; only run once per session
- Other notebooks reuse cached data; should be fast (~2-5 min each)

---

## 7. Modifying the Pipeline

### Add a New Analysis
1. Create new notebook: `notebooks/My-Analysis.ipynb`
2. Cell 1: Import data loaders
   ```python
   from src.data_loaders import load_human_master, load_model_master
   human_master = load_human_master()
   model_master = load_model_master()
   ```
3. Cell 2+: Your analysis code
4. Last cell: Save results to `outputs/`

### Modifying Existing Analysis
- Change **data loading**: Edit `src/data_loaders.py`, all notebooks auto-update
- Change **analysis logic**: Edit specific notebook (e.g., Main-Analysis.ipynb)
- Add **new plots**: Edit that notebook, save to `outputs/`

---

## 8. Key Modules & Imports

### Data Access
```python
from src.config import get_paths
from src.data_loaders import load_human_master, load_model_master, load_bio_master

paths = get_paths()  # returns ProjectPaths(data_dir, outputs_dir, reports_dir)
human_df = load_human_master()  # 39,000 rows × 11 cols
model_df = load_model_master()  # 39,000 rows × 11 cols
bio_df = load_bio_master()      # 39,000 rows × 16 cols (BIO metrics)
```

### Notebook Utilities
```python
from notebooks._utils import get_data_dir  # legacy; use src.config instead
import seaborn as sns
import matplotlib.pyplot as plt

# All notebooks auto-save plots to outputs/ via paths.outputs_dir
```

---

## 9. File Descriptions

| File | Purpose | When to Use |
|------|---------|------------|
| `src/config.py` | Path management | Always first: `get_paths()` |
| `src/data_loaders.py` | Data loading (human, model, BIO) | Every analysis notebook |
| `notebooks/_utils.py` | Legacy utilities | Backward compat; prefer `src/data_loaders` |
| `environment.yml` | Conda dependencies | `conda env create -f environment.yml` |
| `.env` | Local config (DATA_DIR) | Must be set before running notebooks |
| `.gitignore` | Git exclusions | Do not edit; data/ and outputs/ already ignored |

---

## Summary Checklist

- [ ] Conda environment created & activated: `conda activate flexwisdom`
- [ ] `.env` file created with `DATA_DIR` set
- [ ] Data structure verified (50_50, 80_20, 100_0 folders with CSVs)
- [ ] Data access test passed: `from src.config import get_paths; get_paths()`
- [ ] Run **Data-Preparation.ipynb** ✓
- [ ] Run **Main-Analysis.ipynb** ✓
- [ ] Run **Individual-Differences.ipynb** ✓
- [ ] Run **Model-Comparison.ipynb** ✓
- [ ] (Optional) Run **Appendix-BIO-Analysis.ipynb** ✓
- [ ] Results in `outputs/` ✓
- [ ] Share findings! 🎉

---

**Ready? Start with `Data-Preparation.ipynb`!**
