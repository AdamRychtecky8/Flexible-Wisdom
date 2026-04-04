# Ensemble Decision-Making Under Correlation: Humans vs. LLM Groups

**Undergraduate honors thesis research · UCSB Vision & Image Understanding Lab · January 2026**

---

## Research Question

How do human and large language model ensembles compare in collective decision accuracy on a controlled perceptual task — and why do ensemble gains plateau far earlier than the Condorcet Jury Theorem predicts? Using a dataset of 507,600 trials across 12 humans and 12+ LLMs on identical stimuli, this project measures where majority voting fails, identifies error correlation as the mechanistic explanation, and proposes a follow-up study testing whether LLMs can detect and compensate for redundancy in correlated agent groups.

---

## Why This Matters for Intelligent Systems

Most deployed ensemble and multi-agent AI systems assume that combining more agents always helps — an assumption grounded in the Condorcet Jury Theorem, which predicts accuracy approaching 100% as group size grows, *under the assumption of agent independence*. This research shows that assumption is routinely violated in practice: 35–40% of LLM pairs in this dataset share high error correlation (r > 0.5), meaning they fail on the same trials and provide redundant rather than independent evidence. This correlation structure — not accuracy heterogeneity — is what causes ensemble gains to saturate at group sizes far smaller than theory predicts. The findings have direct implications for mixture-of-experts architectures, AI committee systems, and human-AI teaming, where naive aggregation can produce false confidence in redundant agreement.

---

## Key Findings

- **Ensemble voting improves accuracy by 8–15%** over single agents (groups of 12 vs. individuals), depending on task difficulty — consistent with Condorcet predictions at small group sizes
- **Gains plateau sharply at n ≈ 7**: adding agents 8–12 contributes only ~1–2% additional improvement, well below the theoretical curve
- **Weighted Linear Combination (WLC) beats majority voting by +3.3%** (mean accuracy 0.748 vs. 0.724) with lower variance (SD 0.015 vs. 0.018), using 10-fold cross-validation
- **35–40% of LLM pairs show high pairwise error correlation (r > 0.5)**; only 10–15% show near-independence (r < 0.2) — the ensemble is substantially redundant
- **Humans: 47–87% accuracy across conditions** (d′ = 0.35 → 1.02); **LLMs: 48–85%** (d′ = 0.17 → 1.18) — LLMs match or slightly exceed average human performance but with greater heterogeneity (SD 0.08–0.12 vs. 0.06–0.10)
- **Both human and LLM groups underperform the Bayesian Ideal Observer** (BIO ceiling: 85% in the easiest condition; human group: 81%; LLM group: 79%) — indicating room for better aggregation strategies
- **Error correlation explains the plateau**: WLC's +3.3% gain over majority voting traces to the same heterogeneity that the correlation analysis reveals — the learned weights implicitly track which agents are redundant

---

## What Makes This Unusual

**507,600 trials across humans and LLMs on identical stimuli** — not a benchmark comparison but a controlled experiment where every agent sees the same perceptual problem under the same difficulty conditions. The analysis goes beyond accuracy to Signal Detection Theory metrics (d′, criterion, hit/false-alarm decomposition), giving a richer account of *how* agents succeed and fail, not just how often. The mechanistic focus on error correlation as the limiting factor is underexplored in the ensemble literature, which typically assumes or enforces independence. The proposed Phase 2 study (Correlation Blindness) directly tests a behavioral hypothesis about LLM meta-cognition: when explicitly told that agents are correlated, do LLMs discount redundant votes — or do they treat 10 correlated "yes" votes as 10 independent confirmations?

---

## Repository Structure

```
├── notebooks/                         # Analysis pipeline (run in order)
│   ├── Data-Preparation.ipynb         # [1] Load & validate 507,600-trial dataset (~2 min)
│   ├── Main-Analysis.ipynb            # [2] Majority voting bootstrap, WLC, SDT metrics (~5 min)
│   ├── Individual-Differences.ipynb   # [3] Per-participant/model performance & outliers (~2 min)
│   ├── Model-Comparison.ipynb         # [4] Pairwise error correlation & model agreement (~2 min)
│   └── Appendix-BIO-Analysis.ipynb    # [5] Bayesian Ideal Observer benchmark (optional)
│
├── reports/
│   ├── REPORT-BASELINE-ANALYSIS.md    # ← Full written report (10 sections, ~10 pages)
│   └── Report-Baseline-Analysis.ipynb # Interactive version of the same report
│
├── src/
│   ├── config.py                      # Path management & .env parsing
│   └── data_loaders.py                # Centralized loaders: load_human_master(),
│                                      #   load_model_master(), load_bio_master()
│
├── outputs/                           # Generated figures and CSVs
│   ├── baseline_ensemble_gains.png    # Accuracy vs. group size (majority voting)
│   ├── baseline_error_correlation.png # Pairwise error correlation matrix
│   ├── baseline_individual_performance.png
│   ├── baseline_weighted_aggregation.png
│   ├── model-accuracy-ranking.pdf     # Model performance bar chart (publication quality)
│   ├── model-agreement-heatmap.pdf    # Pairwise model agreement
│   ├── model-error-correlation.pdf    # Error correlation heatmap
│   └── model-condition-performance.pdf
│
├── docs/
│   ├── QUICKSTART.md                  # Setup and execution walkthrough
│   ├── PROJECT_OVERVIEW.md            # Research context and task description
│   └── FUTURE_DIRECTIONS.md          # Research trajectory and next directions
│
├── RESEARCH_CONTEXT.md                # Theoretical framing and literature context
├── environment.yml                    # Conda environment (Python 3.11 + dependencies)
└── data/raw/                          # Raw dataset (git-ignored, private)
    ├── 50_50/                         # Hard condition: cue validity = 50%
    ├── 80_20/                         # Medium condition: cue validity = 80%
    └── 100_0/                         # Easy condition: cue validity = 100%
```

---

## Report

**[`reports/REPORT-BASELINE-ANALYSIS.md`](reports/REPORT-BASELINE-ANALYSIS.md)** — Full baseline analysis report (~10 pages). Covers dataset composition, individual and group performance tables, SDT metrics, WLC cross-validation results, pairwise error correlation analysis, the correlation blindness hypothesis, and proposed follow-up study design. Written for advisor review and as a thesis chapter draft.

The baseline report includes a full Phase 2 study design: 3 agent compositions × 2 transparency conditions (blind vs. correlation-disclosed) × 3 LLMs (GPT-4o, Claude-3.7-Sonnet, Gemini-2.5-Pro) = 1,800 API calls, with power analysis (Cohen's d ≈ 0.4–0.6, n=300 trials per condition) and pre-registered outcome scenarios.

---

## Methods Overview

**Task:** 2-alternative forced-choice (2AFC) target-detection with spatial cues. Agents report whether a target is present or absent; cue validity varies by condition (50%, 80%, 100%) to manipulate task difficulty.

**Aggregation methods:**
- Majority voting with bootstrap resampling (500 samples, group sizes 1–12)
- Weighted Linear Combination (WLC) optimized via 10-fold cross-validation
- Bayesian Ideal Observer (BIO) computed from angle estimation data as theoretical upper bound

**Statistical framework:**
- Signal Detection Theory: d′ (discriminability), criterion (response bias), hit rate, false alarm rate — with log-linear correction for extreme rates
- Pairwise error correlation: Pearson correlation on binary error vectors across all model pairs
- Bootstrap confidence intervals throughout

**Data pipeline:** `Data-Preparation.ipynb` → `Main-Analysis.ipynb` → `Individual-Differences.ipynb` → `Model-Comparison.ipynb` → (optional) `Appendix-BIO-Analysis.ipynb`. All notebooks import from `src/data_loaders.py` — single source of truth for data loading.

---

## Reproducibility

```bash
# 1. Create environment
conda env create -f environment.yml
conda activate flexwisdom

# 2. Configure data path
cp .env.example .env
# Edit .env: set DATA_DIR=/path/to/data/raw

# 3. Verify setup
python -c "from src.config import get_paths; get_paths()"

# 4. Run notebooks in order
# notebooks/Data-Preparation.ipynb → Main-Analysis.ipynb → ...
```

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md) for full setup walkthrough.

---

## Tech Stack

Python 3.11 · pandas · numpy · scipy · scikit-learn · statsmodels · matplotlib · seaborn · Jupyter · LLM APIs (GPT-4o, Claude, Gemini)

---

## Status

**Phase 1 — Baseline Analysis: Complete (January 2026)**
Full pipeline implemented; report written; results reproduced and documented.

**Phase 2 — Correlation Blindness Study: Proposed**
Full experimental design (1,800 LLM API calls across GPT-4o, Claude-3.7-Sonnet, Gemini-2.5-Pro), power analysis, and pre-registered outcome scenarios detailed in [`reports/REPORT-BASELINE-ANALYSIS.md`](reports/REPORT-BASELINE-ANALYSIS.md) §4. Pending advisor approval.
