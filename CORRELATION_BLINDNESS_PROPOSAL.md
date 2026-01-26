# Research Proposal: Testing Correlation Blindness in LLM Aggregation Systems

**Project:** Flexible Wisdom — Human-LLM Collective Decision-Making  
**Phase:** Follow-up study after baseline analysis  
**Timeline:** 5–6 weeks (February–March 2026)  
**Budget:** ≤$700 total project budget; $250–350 allocated to this phase  
**Investigator:** Undergraduate Honors Thesis, UCSB Vision & Image Understanding Lab

---

## 1. Background & Motivation

### 1.1 What We've Established (Baseline Analysis)

Our completed baseline analysis ([Report-Baseline-Analysis.md](reports/REPORT-BASELINE-ANALYSIS.md), [Main-Analysis.ipynb](notebooks/Main-Analysis.ipynb)) processed **507,600 trials** (39,600 human + 468,000+ LLM) across a 2-alternative forced-choice target-detection task. Key empirical findings:

1. **Ensemble voting improves performance:** Groups of 12 agents outperform single agents by 8–15% depending on task difficulty
2. **Gains plateau early:** Adding agents beyond n≈7 yields diminishing returns (+1–2%)
3. **Weighted aggregation helps modestly:** Learned WLC weights improve over uniform voting by +3%, but mechanism is unclear
4. **Model correlation is pervasive:** Pairwise error correlation analysis ([Model-Comparison.ipynb](notebooks/Model-Comparison.ipynb)) reveals:
   - 35–40% of model pairs show high error correlation (r > 0.5)
   - 45–50% show moderate correlation (r = 0.2–0.5)
   - Only 10–15% show near-independence (r < 0.2)

**Interpretation:** Standard aggregation methods (majority voting, simple averaging) treat all agents as independent. When agents make *correlated* errors, this assumption fails, causing ensembles to overweight redundant information.

### 1.2 Theoretical Grounding

The **Condorcet Jury Theorem** (Condorcet, 1785) predicts that majority voting approaches 100% accuracy as group size increases—*under the assumption of agent independence*. When this assumption is violated:

- **Brown (2004):** Correlated errors in neural network ensembles eliminate diversity benefits
- **Zhou (2012):** Ensemble accuracy is bounded by the correlation structure of errors
- **Sorkin & Dai (2010):** Human groups fail to discount redundant information from correlated sources
- **Kording & Wolpert (2006):** Optimal Bayesian aggregation requires downweighting correlated evidence

Despite extensive literature on ensemble methods, a critical gap remains: **Do language models—when prompted to aggregate agent decisions—recognize and compensate for correlation without explicit training?**

### 1.3 The Correlation Blindness Hypothesis

**Hypothesis:** When asked to aggregate decisions from multiple agents, large language models exhibit *correlation blindness*: they fail to recognize or discount redundancy in correlated agent groups, leading to:
- Overconfidence when correlated agents agree
- Suboptimal weighting compared to Bayesian-optimal aggregation
- Behavior similar to documented human biases (Sorkin & Dai, 2010)

**Key clarification:** This is *not* a claim about LLM training or architecture. It is a *behavioral* hypothesis about decision-making under uncertainty when given explicit descriptions of agent outputs.

---

## 2. Research Questions

**Primary Question:**  
When explicitly informed about agent correlation structure, do LLMs adjust their aggregation strategy to discount redundant information?

**Secondary Questions:**
1. Is correlation blindness universal across LLM families (GPT, Claude, Gemini) or architecture-specific?
2. How does transparency (telling the model about correlation) affect aggregation quality?
3. Do LLMs produce reasoning traces that reflect Bayesian principles or naive voting heuristics?

---

## 3. Experimental Design

### 3.1 Leveraging Existing Data

**Critical advantage:** We do not need new human trials. We use *empirically measured* error correlations from our existing dataset (507,600 trials) to construct realistic agent scenarios.

**Agent selection procedure:**
1. Use [Model-Comparison.ipynb](notebooks/Model-Comparison.ipynb) error correlation matrix
2. Define agent groups based on **empirical error overlap patterns**:
   - **High-correlation cluster:** 3–4 models with pairwise error correlation r > 0.6
   - **Moderate-correlation cluster:** 3–4 models with 0.3 < r < 0.5
   - **Low-correlation (diverse) cluster:** 3–4 models with r < 0.3

**Trial selection:**
- Sample 100 trials uniformly from existing dataset, stratified by difficulty:
  - 50 trials from high-difficulty condition (50_50, where individual accuracy ≈ 55%)
  - 30 trials from medium-difficulty condition (80_20)
  - 20 trials from easy condition (100_0)
- **Secondary analysis:** Subset of trials where correlated clusters show agreement (to maximize statistical power for detecting transparency effects)

### 3.2 Experimental Conditions

**Independent Variables:**

1. **Agent group composition** (within-subjects):
   - Condition A: 5 highly correlated agents
   - Condition B: 3 correlated + 2 diverse agents  
   - Condition C: 5 diverse agents

2. **Transparency manipulation** (between-subjects):
   - **Blind:** "Here are 5 agent decisions on this trial..."
   - **Transparent:** "Note: Agents A, B, C belong to the same empirical error cluster (historically correlated on 60% of error trials). Agents D, E show independent error patterns."
   - **Control:** "All agents were evaluated on separate validation sets" (placebo transparency)

3. **Ground truth availability** (control):
   - Aggregation prompts do *not* include correctness labels
   - Post-hoc: Compare LLM aggregation to known trial outcomes

**Dependent Variables:**

1. **Aggregation accuracy:** Does LLM's final decision match ground truth?
2. **Effective vote allocation:** How many effective votes does the LLM assign to each agent/cluster? (Structured output required; see Section 3.3)
3. **Confidence calibration:** Does LLM express lower confidence when correlated agents agree vs. diverse agents agree?
4. **Empirical alignment:** How close is LLM vote allocation to empirical stacking baseline (logistic regression trained on held-out data)?

### 3.3 Prompt Structure

**Example prompt (Transparent condition):**

```
You are an expert at aggregating decisions from multiple AI systems.

TASK: Five AI models evaluated this image for target presence. Your job is to 
make a final decision: is the target present or absent?

AGENT DECISIONS:
- Model A: Present
- Model B: Present  
- Model C: Present
- Model D: Absent
- Model E: Absent

IMPORTANT CONTEXT:
Models A, B, and C belong to the same empirical error cluster—they have historically 
correlated error patterns (failing together on ~60% of difficult trials in this task). 
Models D and E show independent error patterns.

INSTRUCTIONS:
1. Assign EFFECTIVE VOTE COUNTS to each agent or agent cluster.
   - If agents are independent, each gets 1 vote.
   - If agents are correlated, discount them (e.g., "A/B/C count as 1 vote total").
   - Your vote counts must sum to a sensible total (e.g., 3 effective votes from 5 agents).

2. Based on your vote allocation, provide your final decision: Present or Absent

3. Explain your reasoning (2-3 sentences)

4. Rate your confidence (0-100%)

OUTPUT FORMAT (required):
{
  "effective_votes": {"A": X, "B": Y, "C": Z, "D": W, "E": V},
  "decision": "Present" or "Absent",
  "reasoning": "...",
  "confidence": 0-100
}
```

**Control variations:**
- **Blind:** Remove "IMPORTANT CONTEXT" section; instruct to assign votes based on decision pattern only
- **Placebo:** Replace with "All models were evaluated on separate validation sets"

### 3.4 Sample Size & Power

**Target sample (MVP design):**
- 100 unique trials × 3 agent compositions = 300 scenarios
- 2 transparency conditions (Blind vs Transparent; within-subjects design)
- **2–3 LLM models tested** (e.g., GPT-4o, Claude-3.7-Sonnet, Gemini-2.5-Pro)
  - Prioritize models from different providers (OpenAI, Anthropic, Google)
  - Allows within-model replication and cross-model comparison

**Total prompts:** 300 scenarios × 2 conditions × 3 models = **1,800 LLM calls**

**Expected effect size:**  
If LLMs are correlation-blind, we predict:
- Transparent condition improves accuracy by 5–10% (Cohen's d ≈ 0.4–0.6)
- Effective vote allocation shifts: correlated clusters receive fewer votes (e.g., 3 agents → 1 effective vote)

With n=300 trials per condition per model, power analysis (α=0.05, β=0.20) detects effects d ≥ 0.3.

---

## 4. Empirical Stacking Baseline

To evaluate LLM aggregation performance, we construct an **empirical stacking baseline** trained on held-out data.

**Method:**
- Use logistic regression to learn optimal aggregation weights from historical trial outcomes
- Input: Binary decisions from each agent (5-dimensional feature vector)
- Output: Probability of target presence
- Training: 80% of trials (held-out from LLM aggregation test set)
- Validation: 20% of trials (same trials used for LLM evaluation)

**Rationale:**  
This is a *data-driven oracle* that learns which agent combinations are empirically effective, accounting for correlation structure implicitly. It represents achievable performance given our dataset, not a theoretical optimum.

**Comparison baselines:**
1. **Naive majority voting:** Each agent gets 1 vote (correlation-blind)
2. **Empirical stacking:** Learned weights from held-out data (correlation-aware)
3. **Effective-N discounting:** Theoretical baseline using cluster structure

**Evaluation metric:**  
We compare LLM aggregation accuracy to:
- Majority voting (should beat this if correlation-sensitive)
- Empirical stacking (approaches this if optimally sensitive)
- Measure vote allocation alignment with stacking weights (as secondary analysis)

---

## 5. Hypothesis Testing

**Null Hypothesis (H₀):** LLMs are correlation-blind  
- Transparent condition has no effect on accuracy
- Effective vote allocation is uniform (each agent gets 1 vote) regardless of correlation structure
- Confidence does not adjust for redundancy

**Alternative Hypothesis (H₁):** LLMs recognize correlation  
- Transparent condition improves accuracy by ≥5%
- Correlated agent clusters receive fewer effective votes (e.g., 3 agents → 1 effective vote)
- Confidence decreases when correlated agents agree vs diverse agents

**Statistical tests:**
1. **Paired t-test:** Accuracy (Blind vs Transparent) within each LLM
2. **ANOVA:** Effect of agent composition (high vs moderate vs low correlation)
3. **Regression:** Effective_votes(cluster) = β₀ + β₁(Correlation) + β₂(Transparency) + ε
4. **Accuracy comparison:** Does LLM aggregation approach empirical stacking baseline in Transparent condition?

---

## 6. Controls & Robustness Checks

**Potential confounds:**

1. **LLM response biases:**  
   - **Control:** Counterbalance trial order; randomize agent labels (A/B/C/D/E)
   - **Test:** Check if LLMs favor certain agent positions (primacy/recency effects)

2. **Transparency phrasing effects:**  
   - **Control:** Use 2–3 transparency phrasings; test for phrasing × accuracy interaction
   - **Test:** Ensure effect isn't driven by keyword priming ("correlated errors" → bias)

3. **Agent identity effects:**  
   - **Control:** Use anonymous labels ("Model A"); no identifying information
   - **Test:** Verify results generalize across different agent label assignments

4. **Task difficulty:**  
   - **Control:** Stratify trials by difficulty (easy/medium/hard)
   - **Test:** Interaction between difficulty and correlation sensitivity

5. **Output format compliance:**
   - **Control:** Validate that LLMs produce parseable JSON with vote counts
   - **Test:** Measure compliance rate; exclude malformed responses

**Validation:**
- **Held-out test set:** Reserve 20% of trials; report final accuracy only on held-out data
- **Cross-model consistency:** If effect is real, it should replicate across 2–3 LLMs
- **Human baseline (optional):** If budget and time allow, recruit 10 human participants for same task to contextualize LLM behavior

---

## 7. Budget & Feasibility

### 7.1 Cost Breakdown

**LLM API costs (primary expense):**

| Model | Cost/1K tokens | Avg tokens/prompt | Calls | Total Cost |
|-------|----------------|-------------------|-------|------------|
| GPT-4o | $0.005 (in) $0.015 (out) | 450 in, 250 out | 600 | $6.75 |
| Claude-3.7-Sonnet | $0.003 (in) $0.015 (out) | 450 in, 250 out | 600 | $5.40 |
| Gemini-2.5-Pro | $0.00125 (in) $0.005 (out) | 450 in, 250 out | 600 | $1.69 |

**Total API cost (1,800 calls):** $13.84  
**With 30% buffer** (retries, debugging, prompt tuning): **$18**

**MVP Design Budget:**
- **Primary experiment:** 1,800 calls × $0.008/call average = $14.40
- **Robustness checks:** 300 additional calls (prompt variants, placebo) = $2.40
- **Pilot testing:** 100 calls = $0.80
- **Buffer (30%):** $5.30

**Total API cost:** **$150–200** (conservative estimate)

**Additional costs:**
- **Compute:** $0 (using existing lab infrastructure)
- **Human validation (OPTIONAL):** $50 if requested (10 participants × $5 gift cards)
- **Miscellaneous:** $25 (data storage, unexpected API charges)

**Total budget for this phase (MVP):** **$175–225**  
**With optional human baseline:** **$225–275**  
**Remaining budget:** $425–525 for follow-up analyses, extended models, or thesis revisions

### 7.2 Timeline

| Week | Tasks | Hours/week |
|------|-------|------------|
| **1** | Prompt engineering, pilot testing (n=50 trials, 1 model), debug pipeline | 15 hrs |
| **2** | Data collection (3,000 LLM calls), logging, quality checks | 10 hrs |
| **3** | Statistical analysis, weight extraction from reasoning traces | 12 hrs |
| **4** | Robustness checks, held-out validation, human baseline comparison | 10 hrs |
| **5** | Figure generation, draft writing, advisor review | 12 hrs |
| **6** | Revisions, supplementary analyses, final submission prep | 8 hrs |

**Total:** ~67 hours over 6 weeks (12 hrs/week average)

**Feasibility:** This fits comfortably within an undergraduate thesis timeline. No complex infrastructure required—uses existing Python pipeline, standard statistical tests, and commercial LLM APIs.

---

## 8. Expected Outcomes & Interpretation

### 8.1 Scenario A: LLMs Are Correlation-Blind (H₀ Supported)

**Expected results:**
- Transparent condition shows no accuracy improvement (< 2%)
- Effective vote distributions remain uniform (each agent gets ~1 vote)
- Confidence does not adjust for correlation structure

**Interpretation:**
- LLMs lack implicit recognition of evidence redundancy
- Aggregation systems need *explicit correlation detection* algorithms
- Behavior mirrors documented human biases (Sorkin & Dai, 2010)

**Contribution:**  
Identifies a systematic limitation in LLM reasoning about aggregation; motivates development of correlation-aware prompting strategies or explicit preprocessing modules.

### 8.2 Scenario B: LLMs Recognize Correlation (H₁ Supported)

**Expected results:**
- Transparent condition improves accuracy by 5–10%
- Correlated agents receive fewer effective votes (e.g., 3 agents → 1 vote)
- LLM aggregation accuracy approaches empirical stacking baseline

**Interpretation:**
- LLMs can discount redundant evidence when correlation structure is made explicit
- Transparency prompts enable more sophisticated aggregation strategies
- Effect likely generalizes across strong LLMs (GPT-4o, Claude, Gemini)

**Contribution:**  
Demonstrates that LLMs can implement correlation-aware aggregation via natural language prompting alone; suggests new methods for human-AI decision support systems.

### 8.3 Scenario C: Partial Recognition (Mixed Results)

**Expected results:**
- Effect is model-dependent (e.g., newer models sensitive, smaller models blind)
- Effect is condition-dependent (e.g., works for high correlation, fails for moderate)
- Vote adjustment is qualitative ("I'll count A/B/C as one source") but not optimally calibrated

**Interpretation:**
- Correlation sensitivity may scale with model capacity or training approach
- Prompting format matters (explicit cluster information vs implicit inference)
- Current LLMs show emerging but incomplete correlation awareness

**Contribution:**  
Maps the landscape of LLM aggregation capabilities across 2–3 representative models; identifies which architectures are suitable for decision support applications.

---

## 9. Limitations & Scope

### 9.1 What This Study Does NOT Do

1. **Train or fine-tune models:** We test *pretrained* LLMs via prompting only
2. **Claim architectural insights:** This is a behavioral study, not a mechanistic investigation
3. **Solve the aggregation problem:** We test whether LLMs recognize correlation; we do not build a production system
4. **Generalize beyond binary tasks:** Results apply to binary decisions (present/absent); extension to continuous or multi-class tasks requires separate validation
5. **Claim causality about training data:** We cannot determine *why* LLMs are/aren't correlation-sensitive without access to training corpora

### 9.2 Threats to Validity

**Internal validity:**
- **Prompt sensitivity:** Results may depend heavily on phrasing; we mitigate via 3 transparency variants
- **Agent selection bias:** Choosing specific models may not represent full correlation spectrum; we sample across empirical correlation distribution

**External validity:**
- **Task-specific:** Target-detection task may not generalize to text, forecasting, or medical domains
- **LLM-specific:** Results apply to 2025-2026 LLM generations; newer models may differ

**Construct validity:**
- **"Correlation" defined empirically:** We use observed error overlap, not causal correlation (agents weren't trained together)
- **"Understanding" inferred from behavior:** We cannot directly observe internal representations

### 9.3 Ethical Considerations

- **No human subjects required:** Primary study uses only LLM API calls
- **Optional human validation:** If conducted, involves minimal risk (20 min, $5 compensation, IRB-exempt)
- **No deceptive framing:** Transparency prompts accurately describe empirical error correlations from historical data
- **Transparent reporting:** All data, code, prompts, and results will be shared in public repository

---

## 10. Contribution to Literature

### 10.1 Positioning in Existing Work

**Ensemble learning (ML perspective):**
- Extends Brown (2004), Zhou (2012) to LLM aggregation
- Tests whether diversity-accuracy tradeoff applies to prompted systems

**Collective intelligence (psychology perspective):**
- Extends Surowiecki (2004), Sorkin & Dai (2010) to AI systems
- Compares human vs LLM sensitivity to correlation

**LLM reasoning (AI alignment perspective):**
- Tests whether LLMs implicitly implement Bayesian decision theory (Kording & Wolpert, 2006)
- Identifies potential systematic biases in AI advisory systems

### 10.2 Novel Contributions

1. **First behavioral test of correlation blindness in LLMs** (to our knowledge)
2. **Uses real error correlation structure** from large-scale human-AI dataset (not synthetic)
3. **Compares LLM behavior to Bayesian optimal** (not just accuracy)
4. **Tests transparency as intervention** (practical implication for prompting strategies)

### 10.3 Publication Venue

**Target:** Workshop paper at NeurIPS, ICML, or AAAI (Collective Intelligence track)  
**Backup:** Cognitive Science Society, Human Factors & Ergonomics Society  
**Thesis:** Full chapter with extended analysis and human baseline comparison

---

## 11. Integration with Broader Project

### 11.1 How This Builds on Baseline Analysis

- **Reuses infrastructure:** Data loaders, SDT metrics, plotting functions ([src/data_loaders.py](src/data_loaders.py))
- **Leverages empirical findings:** Error correlation matrix ([Model-Comparison.ipynb](notebooks/Model-Comparison.ipynb))
- **Extends ensemble analysis:** Connects WLC performance to correlation structure ([Main-Analysis.ipynb](notebooks/Main-Analysis.ipynb))

### 11.2 Path to Future Work

If correlation blindness is confirmed:
- **Phase 3:** Develop correlation-aware prompting strategies (fine-tuning?)
- **Phase 4:** Test on human-AI teams (do humans + LLMs compound biases?)
- **Phase 5:** Build production decision-support system with explicit correlation modeling

If LLMs are correlation-sensitive:
- **Phase 3:** Map which transparency formats maximize Bayesian alignment
- **Phase 4:** Test on complex domains (medical diagnosis, forecasting)
- **Phase 5:** Deploy LLM-based aggregation in real-world advisory systems

---

## 12. Success Criteria

**Minimum viable result (MVP):**
- Clean effect (p < 0.05) in at least 2/3 LLMs
- Effective vote allocation shifts significantly in Transparent condition
- LLM aggregation accuracy improves over naive majority voting
- Advisor approval to move to thesis writing

**Strong result:**
- Effect size d > 0.5 across all tested LLMs
- Transparent condition improves accuracy by ≥7%
- LLM aggregation approaches empirical stacking baseline (within 3–5%)

**Publication-ready result:**
- Effect replicates across trial difficulty levels (easy/medium/hard)
- Robustness checks pass (no confounds, held-out validation accurate)
- Structured output analysis reveals interpretable vote allocation patterns
- Optional: Human baseline shows similar or stronger correlation blindness

---

## 13. References

Brown, G. (2004). Diversity in neural networks for classification. *Machine Learning*, 57(3), 233–247.

Condorcet, J. A. N. (1785). *Essay on the Application of Analysis to the Probability of Majority Decisions*. Paris: Imprimerie Royale.

Kording, K. P., & Wolpert, D. M. (2006). Bayesian decision theory in neuroscience. *Trends in Cognitive Sciences*, 10(12), 529–535.

Sorkin, R. D., & Dai, H. (2010). Signal detection analysis of the ideal group. *Organizational Behavior and Human Decision Processes*, 113(2), 154–166.

Surowiecki, J. (2004). *The Wisdom of Crowds: Why the Many Are Smarter Than the Few*. Doubleday.

Zhou, Z. H. (2012). *Ensemble Methods: Foundations and Algorithms*. CRC Press.

---

## 14. Appendix: Sample Prompts

### A.1 Blind Condition (No Transparency)

```
You are an expert at aggregating decisions from multiple AI systems.

TASK: Five AI models evaluated an image for target presence. Based on their 
decisions, determine: is the target present or absent?

AGENT DECISIONS:
- Model A: Present
- Model B: Present
- Model C: Present
- Model D: Absent
- Model E: Absent

INSTRUCTIONS:
1. Assign EFFECTIVE VOTE COUNTS to each agent.
   - If you treat agents equally, assign 1 vote each.
   - If you believe some agents are redundant or unreliable, adjust vote counts.
   - Your vote counts should sum to a sensible total.

2. Based on your vote allocation, provide your final decision: Present or Absent?

3. Explain your reasoning (2-3 sentences)

4. Rate your confidence (0-100%)

OUTPUT FORMAT (required):
{
  "effective_votes": {"A": X, "B": Y, "C": Z, "D": W, "E": V},
  "decision": "Present" or "Absent",
  "reasoning": "...",
  "confidence": 0-100
}
```

### A.2 Transparent Condition (Correlation Disclosed)

```
[Same as above, plus:]

IMPORTANT CONTEXT:
Models A, B, and C belong to the same empirical error cluster—they have historically 
shown correlated error patterns (failing together on ~60% of difficult trials in this 
task). Models D and E show independent error patterns.

Remember to assign effective vote counts that account for this correlation structure.

[Rest identical]
```

### A.3 Placebo Control (False Transparency)

```
[Same as Blind, plus:]

IMPORTANT CONTEXT:
All five models were evaluated on separate held-out validation sets.

[Rest identical]
```

---

**Proposal Status:** Ready for advisor review  
**Next Steps:** 
1. Advisor approval
2. Pilot study (Week 1)
3. IRB exemption confirmation (human validation)
4. Full data collection (Weeks 2–3)

**Contact:** [Student Name], UCSB Vision & Image Understanding Lab  
**Advisor:** [Advisor Name]  
**Date Prepared:** January 25, 2026
