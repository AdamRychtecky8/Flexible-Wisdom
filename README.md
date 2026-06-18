# Ensemble Decision-Making Under Correlation: Humans vs. LLM Groups

Undergraduate honors thesis research began with UCSB Vision and Image Understanding Lab completed privately. Big thanks to Parsa Madinei for providing the dataset and guidance in the initial stages.

## What this is

A controlled comparison of how human groups and large language model groups make collective decisions on the same perceptual task. Twelve people and twelve LLM agents each judged the same two-alternative forced-choice target-detection problem under three difficulty levels, 72,000 decisions in total, with known ground truth on every trial. The dataset was provided by a graduate student collaborator. The analysis here is my own.

## The finding

On an identical task, LLM groups substantially outperform human groups and come within a few points of the Bayesian optimal observer, while human groups stay well below it. Combining more agents helps, but the gains saturate early, by around five agents, for both humans and LLMs. The reason is that agent errors are positively correlated. Agents tend to fail on the same trials, so each added agent contributes less than an independent vote. Treating correlated agreement as if it were independent is the assumption behind the Condorcet Jury Theorem, and behind much of how multi-agent and mixture-of-experts systems are built.

## Why it matters for AI systems

Most ensemble and multi-agent designs assume that adding agents adds independent evidence. This dataset shows that assumption breaking on a clean, controlled task with a diverse set of current models. Errors are positively correlated across agents, with a mean pairwise error correlation around 0.29, so a group of twelve provides meaningfully less than twelve independent votes, and naive vote-counting produces false confidence in redundant agreement. The same effect governs LLM committees, mixture-of-experts routing, and human-AI teaming, where the value of an added agent depends on whether its errors are independent of the ones already in the room.

## Key results

Every figure here is computed from the data and recorded with its source in `reports/VERIFIED_NUMBERS.md`.

- LLM agents beat humans at the individual level in every condition: roughly 0.75 to 0.80 accuracy versus 0.58 to 0.66, with discriminability (d-prime) about two to three times higher.
- At the full twelve-agent ensemble, LLM groups reach 0.835 to 0.884 across conditions. Human groups reach 0.637 to 0.784.
- The Bayesian ideal observer ceiling is 0.886 to 0.920. LLM ensembles land within 3 to 5 points of it. Human ensembles sit 13 to 25 points below.
- Ensemble gains saturate early. The accuracy added per extra agent drops below one point by around five agents, with no sharp cutoff, for both groups.
- Agent errors are weakly to moderately positively correlated. Strong pairwise correlation (r above 0.5) appears in 8 to 14 percent of model pairs depending on condition. No pairs are negatively correlated.

## The result in one figure

![Ensemble accuracy versus group size for human and LLM groups across the three difficulty conditions. The dashed line is the Bayesian ideal observer ceiling. LLM ensembles approach the ceiling while human ensembles fall short, and gains saturate by around five agents.](outputs/headline-ensemble-vs-optimal.png)

For the full analysis, methods, and discussion, see the report: [reports/REPORT.pdf](reports/REPORT.pdf).

## Task and method

**Task.** Two-alternative forced-choice target detection with a spatial cue. Each agent reports whether a target is present. Cue validity sets difficulty: 50 percent (uninformative), 80 percent, and 100 percent. 1,000 trials per agent per condition.

**Agents.** Twelve human participants and twelve LLM agents spanning current GPT, Claude, Gemini, and o-series models. gemini-2.5-pro appears under two readout methods: one that estimated the stimulus angle and mapped it to a decision (`gemini-2.5-pro-angle`), and one that returned the decision directly (`gemini-2.5-pro-decision`). Their elevated mutual correlation is expected, since they share an underlying model.

**Analysis.**
- Majority voting with bootstrap resampling, 500 samples, group sizes 1 to 12.
- Signal Detection Theory: d-prime, criterion, hit and false-alarm rates, with log-linear correction for extreme rates.
- Pairwise error correlation across all agent pairs.
- Bayesian Ideal Observer computed from the true stimulus distributions, as the optimal ceiling.

## Repository

```
notebooks/      Analysis pipeline, run in order:
                Data-Preparation, Main-Analysis, Individual-Differences,
                Model-Comparison, Appendix-BIO-Analysis
src/            config.py, data_loaders.py, bio.py (Bayesian ideal observer)
outputs/        Generated figures and CSVs
reports/        REPORT.qmd            full report (Quarto source)
                REPORT.pdf            full report (rendered)
                VERIFIED_NUMBERS.md   every figure traced to its source
data/           Raw dataset (private, not tracked)
```

`reports/VERIFIED_NUMBERS.md` traces every number in this README back to the notebook or output file that produced it.

## Reproduce

```bash
conda env create -f environment.yml
conda activate flexwisdom
cp .env.example .env          # set DATA_DIR to the data path

# run the notebooks in the order listed above, then render the report
quarto render reports/REPORT.qmd --to pdf
```

## Status

**Phase 1, baseline analysis: complete.** Full pipeline, results computed from data and documented.

**Phase 2, correlation blindness: proposed.** A designed but not yet run follow-up testing whether an LLM acting as the aggregator discounts correlated agents, or treats correlated agreement as independent confirmation. Design in the report (`reports/REPORT.pdf`).

## Tech

Python, pandas, numpy, scipy, scikit-learn, statsmodels, matplotlib, seaborn, Jupyter, Quarto.