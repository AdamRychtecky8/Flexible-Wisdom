# Future Directions: Grounding for Research Evolution

**Date:** January 2026  
**Project Status:** Baseline analysis complete (human vs model majority voting, individual differences, model comparison)  
**Goal:** Define north-star research direction for publication & thesis work

---

## 1. Current Project Foundation

### What We've Completed
✅ **Human Data:** 12 participants × 3 difficulty levels (50_50, 80_20, 100_0) × ~1,100 trials = 39,600 total trials  
✅ **Model Data:** 12+ LLM variants (Gemini, GPT-4o, etc.) × 3 conditions × 13,000 trials = 468,000+ trials  
✅ **Baseline Analysis:**
- Group size effects: Does majority voting improve with group size?
- Weighted Linear Combination (WLC): Can weighted aggregation beat uniform voting?
- Signal Detection Theory (SDT): d' (discriminability), criterion (bias), hit/FA rates
- Individual differences: Per-participant & per-model performance
- Model agreement patterns: Which models are redundant vs. complementary?
- Bayesian Ideal Observer (BIO): Theoretical optimal performance benchmark

### Key Infrastructure Ready
- **src/data_loaders.py:** Centralized data access (no hardcoding, no duplication)
- **Notebook pipeline:** Linear analysis flow (Data-Prep → Main-Analysis → Differences → Comparison → BIO)
- **Outputs:** CSVs, PDFs, aggregation strategies (majority, WLC, BIO)
- **Code modularity:** Easy to add new analyses without touching existing notebooks

### What We Know From Data
1. **Human-Model Alignment:** Humans and individual models have complementary error patterns
2. **Aggregation Matters:** Group voting outperforms individual agents (human or AI) in most conditions
3. **Heterogeneity:** Models vary widely in accuracy, strategy, and correlation with humans
4. **Difficulty Effect:** Performance scales with signal-to-noise ratio (100_0 > 80_20 > 50_50)

---

## 2. Three Niche Research Directions

All three directions:
- **Use existing dataset** (no new human data collection)
- **Fit Flexible-Wisdom infrastructure** (straightforward LLM API calls)
- **Connect to psychology/AI theory** (publishable scope)
- **Are underexplored in literature** (novel angle)

---

### **OPTION 1: Reliability Learning** 
#### *"Can an LLM learn which agents are reliable without seeing ground truth?"*

**Core Question:**  
When an LLM sees *only past agreement/outcomes* between multiple agents (without knowing which decisions were correct), can it learn to trust some agents more than others? Does this mirror how human groups adapt trust?

**Setup:**
1. Hide ground truth from LLM; give it only:
   - Agent decision history (human, model1, model2, ...)
   - Trial-by-trial agreement/disagreement patterns
   - Maybe: confidence signals (but not correctness)

2. Ask LLM to:
   - Identify which agents seem "reliable"
   - Make a new decision leveraging learned trust weights
   - Compare to:
     - Uniform weighting (baseline)
     - Known-truth WLC weights (oracle)
     - Human group behavior (do humans do this?)

3. Test across conditions (easy/hard tasks)

**Why This Works:**
- **Novel angle:** Most aggregation research uses gold-standard labels. This asks: what if you don't have them?
- **Psychological relevance:** Humans learn to trust teammates by observing agreement, not accuracy.
- **Practical:** Real-world aggregation often happens without ground truth (e.g., committee decisions).
- **LLM advantage:** Language models are good at pattern-matching and reasoning about reliability.

**Output:**
- Paper: "Learning Reliability from Agreement: LLMs as Meta-Aggregators"
- Contribution: Theory on how distributed systems self-organize trust

**Estimated Effort:**
- ~$200–300 API spend (many trials × multiple models)
- 4–6 weeks implementation + analysis

---

### **OPTION 2: Correlation Blindness** 
#### *"Do LLMs over-count correlated agents compared to Bayesian aggregation?"*

**Core Question:**  
When multiple agents make *correlated* errors (e.g., 3 models all fail on angle-estimation trials), does an LLM's aggregation "overweight" this redundancy? Does it behave like a naive human or like optimal Bayesian inference?

**Setup:**
1. Identify clusters of agent types:
   - Complementary agents (model + human; different error patterns)
   - Correlated agents (two similar models; shared failure modes)
   - Adversarial agents (one agent is systematically wrong)

2. Create synthetic voting scenarios:
   - Trial A: majority vote = 3 correlated models + 1 human
   - Trial B: majority vote = 2 humans + 2 diverse models
   - Ask LLM: "Which voting group is more trustworthy?"

3. Compare LLM reasoning to:
   - Bayesian prediction (accounts for correlation explicitly)
   - Human group judgments (do they fall into same trap?)
   - Empirical correctness (which group actually performs better?)

**Why This Works:**
- **Underexplored:** Most studies assume agent independence. Correlation is the **real** problem in ensembles.
- **You have the data:** You already identified which models agree/disagree. You just need to formalize "correlation" in your dataset.
- **Cognitive psychology angle:** Links to heuristics (availability, anchoring) and rational bias literature.
- **Actionable:** If LLMs are correlation-blind, that's a genuine limitation worth publishing.

**Output:**
- Paper: "Correlation Blindness in LLM Aggregation: When Agreement ≠ Reliability"
- Contribution: Identified a systematic bias in LLM reasoning about ensemble diversity

**Estimated Effort:**
- ~$150–250 API spend (fewer models, more targeted trials)
- 3–5 weeks implementation + analysis

---

### **OPTION 3: Rule Emergence** 
#### *"Do LLMs converge to human-like rules when asked to aggregate, or invent new ones?"*

**Core Question:**  
When you ask different LLMs to "aggregate agent decisions," do they invent the same rules humans use (majority, confidence-weighted), or do they discover entirely new strategies? Does this vary by model size/training?

**Setup:**
1. Prompt engineering study:
   - Give LLM a *description* of agent decisions (without labels: "Agent 1: yes, confidence 0.8; Agent 2: no, confidence 0.6; ...").
   - Ask: "Which decision should we trust?"
   - Vary instructions (minimal, detailed, adversarial).
   - Collect reasoning across models (GPT-4o, Gemini, Claude, Llama, etc.).

2. Analyze emergent rules:
   - Do they mention majority?
   - Do they weight by confidence?
   - Do they invent new aggregation heuristics?
   - Do they use reasoning about agent expertise?

3. Benchmark against:
   - Actual human group decisions (do humans reason similarly?)
   - Empirical performance (do LLM rules actually work on your test set?)
   - Known-optimal WLC (how close to oracle?)

**Why This Works:**
- **Directly interpretable:** You can read LLM reasoning. It's not a black box.
- **Connects to human-AI alignment:** Understanding LLM "rules" helps us align AI behavior to human values.
- **Scalable:** Easy to test with many models and conditions.
- **Recent literature:** This sits at intersection of mechanistic interpretability + decision theory + behavioral economics.

**Output:**
- Paper: "Emergent Aggregation Rules in Large Language Models: Do They Mirror Human Heuristics?"
- Contribution: Characterization of LLM reasoning about group decisions; implications for human-AI teaming

**Estimated Effort:**
- ~$100–200 API spend (mostly prompt testing, not heavy computation)
- 3–4 weeks implementation + analysis

---

## 3. Recommendation & Rationale

### My Recommendation: **OPTION 2 — Correlation Blindness**

**Why:**
1. **Novelty:** Underexplored in literature. Most ensemble research ignores correlation.
2. **Your data is primed:** You already have the phenomenon (correlated models) but haven't framed it this way.
3. **Publishable scope:** Specific enough for a strong paper, but not niche to the point of irrelevance.
4. **Psychological depth:** Connects to human decision-making, cognitive biases, and rationality.
5. **Cost-efficient:** Fewer expensive API calls than Reliability Learning; more focused than Rule Emergence.
6. **Future-proof:** Result feeds into reliability learning (Option 1) if you continue.

**Alternative Path:**  
If you prefer interpretability and want to "see what LLMs think," **Option 3 (Rule Emergence)** is more engaging and faster to prototype.

---

## 4. Budget & Resources

### Estimated Total Cost: **~$700–1,000**

**Breakdown (for recommended Option 2):**
```
Core analysis ($200–250):
  - Prompt variations across 5 LLM models
  - ~500 trials × 2 conditions (easy/hard correlated groups)
  - GPT-4o: ~$100
  - Gemini: ~$50
  - Claude: ~$50
  - Others (Llama, fine-tuned): ~$50

Validation & re-runs ($150–200):
  - If initial results unclear, refine prompts
  - Test on held-out subset
  - Edge case exploration

Overhead/buffer ($100–150):
  - Prompt engineering iterations
  - Unexpected API limits or throttling
  - Extended analysis if needed
```

**Comparison to Option 1:**
- Option 1 (Reliability Learning) = $300–500 (more LLM calls, more complex prompting)
- Option 3 (Rule Emergence) = $100–150 (fewer models, simpler prompting)

---

## 5. Implementation Plan (Option 2 Recommended)

### Phase 1: Formalize Correlation (Week 1)
- Define "correlated agent cluster" using your existing Model-Comparison.ipynb outputs
- Create taxonomy: complementary vs. correlated vs. adversarial
- Select 3–5 representative trials for each cluster

### Phase 2: Prompt Engineering (Week 1–2)
- Write base prompt: "Here are agent decisions. Which is most trustworthy?"
- Variants:
  - Minimal (no context)
  - Detailed (explain trade-offs)
  - Bayesian-hint (mention correlation)
  - Adversarial (one agent is deliberately wrong)

### Phase 3: LLM Study (Week 2–3)
- Prompt 5 LLMs with ~200 trials each across conditions
- Collect decisions and reasoning
- Log API costs and latency

### Phase 4: Analysis (Week 3–4)
- Quantify: does LLM performance drop on correlated agents?
- Qualitative: extract reasoning rules from LLM outputs
- Compare to Bayesian optimal, human behavior, empirical correctness

### Phase 5: Validation & Writing (Week 4–5)
- Test findings on held-out subset
- Draft paper structure
- Create figures/tables

**Estimated Total Timeline:** 5–6 weeks  
**Effort:** ~15–20 hrs/week (including writing)

---

## 6. Grounding for Future Decisions

### North Star Principle
**All future work on this project must ask:**
> *"Does this advance understanding of how LLMs aggregate correlated agents vs. Bayesian/human baselines?"*

**Yes → Pursue**  
Example: "Can LLMs learn to discount correlated agents if shown a reliability pattern?"

**No → Defer or archive**  
Example: "What if we add a 4th condition?" (Defer unless it directly tests correlation hypothesis)

### Connected Research Threads (Build-Out Order)
1. **Now (Foundation):** Correlation Blindness (Option 2)
2. **Next (If successful):** Reliability Learning (Option 1) — LLMs learning to discount correlated agents
3. **Later (Extended scope):** Rule Emergence (Option 3) — Do LLMs invent new aggregation rules when told about correlation?
4. **Thesis-level:** Human-AI teaming under correlation; implications for real-world ensemble systems

### Avoid Dead-Ends
❌ "More conditions" (50_50, 80_20, 100_0 is enough; difficulty effects are known)  
❌ "More models" (12+ is sufficient; diminishing returns after ~8)  
❌ "Prettier plots" (focus on theory, not aesthetics)  
✅ "What about X agent type?" (only if X reveals something about correlation)

---

## 7. Success Criteria

### For This Report (Next Phase)
- [ ] Demonstrate mastery of baseline dataset (human vs. model behavior)
- [ ] Show understanding of project purpose (collective decision-making, ensemble aggregation)
- [ ] Position correlation blindness as novel angle worth exploring
- [ ] Connect to psychology/AI theory literature

### For Option 2 Full Study (Post-Report)
- [ ] LLMs demonstrate measurable correlation blindness (p < 0.05)
- [ ] Effect size comparable to human overconfidence biases
- [ ] Actionable recommendation for better aggregation systems
- [ ] Publication in top-tier venue (Cognitive Science, Frontiers in AI, or equivalent)

---

## 8. Relevant Literature & Theory

**Correlation Blindness Context:**
- Ensemble diversity (Zhou, 2012: "Ensemble Methods")
- Error correlation in ML (Brown, 2004)
- Human group judgment and redundancy (Surowiecki, 2004: "Wisdom of Crowds" — but with the caveat that correlated crowds are less wise)
- LLM reasoning biases (recent work on heuristics-and-biases in LLMs)

**Key papers to cite:**
1. Brown et al. (2004) "Diversity in neural networks for classification"
2. Surowiecki (2004) "The Wisdom of Crowds" (highlight: *independent* diverse minds)
3. Kording & Wolpert (2006) "Bayesian decision theory in neuroscience"
4. Recent LLM reasoning studies (prompt engineering, in-context learning)

---

## Summary: North Star Statement

**Over the next 6 months, our research will investigate:**

> **"How do LLMs aggregate correlated agent decisions compared to Bayesian-optimal and human-like strategies? And crucially, are they blind to redundancy, leading to overconfidence in correlated groups?"**

**This work:**
- Leverages the 39,600-trial human + 468,000-trial model dataset
- Connects to psychology (group decision-making, cognitive biases)
- Addresses AI safety (ensemble diversity, failure modes)
- Produces publication-quality results with $700–1,000 budget

**Downstream applications:**
- Reliability learning (LLMs detecting trustworthy agents without ground truth)
- Human-AI teaming (when should we trust LLM aggregation vs. human judgment?)
- Mechanistic interpretability (what reasoning rules do LLMs learn?)

---

**Decision Point:** Do you want to proceed with **Option 2 (Correlation Blindness)** as the primary direction, or would you prefer one of the other two options?

Once confirmed, we'll move to Phase 1 of the report: demonstrating mastery of the baseline analysis and positioning this research direction.
