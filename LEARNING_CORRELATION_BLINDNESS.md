# Understanding Correlation Blindness in LLM Aggregation Systems
## A Learning Guide for the Flexible Wisdom Project

**Purpose:** This document explains the theoretical foundations, design choices, and reasoning behind the correlation blindness study. It is written to help you deeply understand *why* the research is structured the way it is, not just *how* to execute it.

**Audience:** You, the researcher. This is your reference for understanding research decisions and thinking through interpretations.

**Date:** January 2026  
**Project:** Flexible Wisdom — Human-LLM Collective Decision-Making

---

## 1. The Big-Picture Question

### 1.1 What Are We Really Asking?

The central scientific question is:

> **When an aggregation system (in this case, an LLM) is asked to combine decisions from multiple agents, does it recognize and appropriately discount redundant information arising from correlated errors?**

This is *not* asking whether LLMs "understand" correlation in some abstract sense. It's asking whether their *behavior* when aggregating decisions reflects sensitivity to a statistical property (correlation) that optimal aggregators should account for.

### 1.2 Why Correlation Matters for Collective Intelligence

The classic **Condorcet Jury Theorem** (1785) says that if you have N independent agents, each with accuracy p > 0.5, then majority voting accuracy approaches 100% as N → ∞.

**The critical assumption:** Independence.

In reality, agents are rarely independent:
- AI models trained on similar datasets make correlated errors
- Human experts in the same field share biases and knowledge gaps
- Sensors measuring the same phenomenon share systematic noise

When agents have correlated errors, you don't get N independent pieces of evidence—you get something closer to k << N effective pieces of evidence. Standard aggregation methods (majority vote, averaging) don't account for this, leading to:

1. **Overconfidence:** Treating 10 correlated "yes" votes as if they're 10 independent confirmations
2. **Diminishing returns:** Adding more correlated agents barely improves performance
3. **Missed opportunities:** Failing to upweight the rare diverse agents who provide genuinely new information

**Key insight from your baseline analysis:** You observed exactly this pattern—ensemble accuracy plateaus early, and error correlation explains why.

### 1.3 Why Test LLMs?

LLMs are interesting test cases for three reasons:

1. **They aggregate naturally via prompting:** You don't need to design algorithms—you can ask them to aggregate in natural language
2. **They handle uncertainty:** LLMs have been trained on reasoning tasks involving evidence combination
3. **They're increasingly used for decision support:** Understanding their limitations matters for real-world deployment

**Important:** This is not anthropomorphizing. You're not asking if LLMs "think" like humans. You're measuring *behavioral* patterns: given inputs (agent decisions + correlation structure), what outputs (aggregation decisions) do they produce?

**Related reading:**
- Surowiecki, J. (2004). *The Wisdom of Crowds*. Chapters 1-2 on independence assumption.
- Condorcet, J. A. N. (1785). *Essay on the Application of Analysis to the Probability of Majority Decisions*.
- Brown, G. (2004). "Diversity in neural networks for classification." *Machine Learning* 57(3). (Shows correlation destroys ensemble benefits in ML systems)

---

## 2. From Dataset to Problem

### 2.1 What Your Dataset Contains

You have **507,600 trials** from a 2-alternative forced choice (2AFC) target detection task:
- **39,600 human trials:** 12 participants, 3 conditions, ~3,300 trials each
- **468,000+ LLM trials:** 12+ models, 3 conditions, ~13,000 trials each

Each trial has:
- **Stimulus properties:** Target presence/absence (TP), cue validity, angle measurements
- **Agent response:** Binary decision (present/absent)
- **Human-only:** Confidence rating (1-7 scale)
- **Ground truth:** Correct answer is known

### 2.2 Why Binary Decisions Are Sufficient

Some might ask: "Don't we need confidence scores to study aggregation?"

**Answer:** No. Here's why:

Correlation is about *error patterns*, not confidence. Two agents are correlated if they fail on the same trials. This is observable from binary outputs alone:

```
Agent A: [1, 0, 1, 0, 1]  (present, absent, present, absent, present)
Agent B: [1, 0, 1, 1, 1]  (present, absent, present, present, present)
Truth:   [1, 0, 1, 1, 1]

Errors A: [0, 0, 0, 1, 0]  (wrong on trial 4)
Errors B: [0, 0, 0, 0, 0]  (perfect)

Error correlation = 0 (they don't fail together)
```

If A and B were correlated:
```
Agent A: [1, 0, 0, 0, 1]
Agent B: [1, 0, 0, 0, 1]
Truth:   [1, 0, 1, 1, 1]

Errors A: [0, 0, 1, 1, 0]
Errors B: [0, 0, 1, 1, 0]

Error correlation = 1.0 (they always fail together)
```

**Key principle:** Aggregation quality depends on *when* agents are wrong relative to each other, not *how confident* they are. Binary decisions capture this.

### 2.3 Representing Agents as Error Vectors

Mathematically, each agent can be represented as an error vector:

$$\mathbf{e}_i = [e_{i,1}, e_{i,2}, \ldots, e_{i,T}]$$

where $e_{i,t} = 1$ if agent $i$ made an error on trial $t$, and $e_{i,t} = 0$ otherwise.

**Pairwise error correlation** between agents $i$ and $j$ is:

$$\rho_{ij} = \text{Pearson correlation}(\mathbf{e}_i, \mathbf{e}_j)$$

This measures how often two agents fail together beyond what chance predicts.

**Why this matters:** High $\rho_{ij}$ means agents provide redundant information. Low or negative $\rho_{ij}$ means they're complementary.

**In your dataset:** You computed this in [Model-Comparison.ipynb](notebooks/Model-Comparison.ipynb) and found 35-40% of model pairs have high correlation (r > 0.5).

---

## 3. Understanding Correlation

### 3.1 What Correlation Means (Math and Intuition)

**Mathematical definition:**  
Correlation measures linear association between two variables. For error vectors:

$$\rho = \frac{\text{Cov}(E_A, E_B)}{\sigma_A \sigma_B}$$

**Intuitive definition:**  
"How predictable is Agent B's error given Agent A's error?"

- $\rho = 1$: If A fails, B always fails (perfect redundancy)
- $\rho = 0$: A's failures don't predict B's failures (independence)
- $\rho = -1$: If A fails, B succeeds (perfect complementarity—rare in practice)

### 3.2 Why Agreement ≠ Independence

**Common misconception:** "If two agents agree 90% of the time, they must be correlated."

**Reality:** Agreement rate includes *correct* agreements and *error* agreements.

Example:
```
Agent A:  [1, 1, 1, 1, 0]
Agent B:  [1, 1, 1, 1, 0]
Truth:    [1, 1, 1, 1, 1]

Agreement: 100% (they always agree)
Shared errors: 1 trial (both wrong on trial 5)
Error correlation: Undefined (need multiple error instances)
```

If both agents are accurate (say 90%), they'll agree most of the time just by both being correct. What matters for correlation is *error overlap*: when A is wrong, is B also wrong?

**Key distinction:**
- **Accuracy:** How often an agent is right
- **Agreement:** How often two agents give the same answer
- **Error correlation:** How often two agents are wrong together

### 3.3 How Correlated Agents Reduce Effective Information

Imagine you have 5 agents voting:
- **Scenario 1 (Independent):** Each agent has 70% accuracy, errors are random
  - Majority vote accuracy ≈ 84% (combining 5 independent signals)
  
- **Scenario 2 (Correlated):** 3 agents are clones (perfect correlation), 2 are independent
  - Effective information = 3 sources, not 5
  - Majority vote accuracy ≈ 78% (worse than scenario 1)

**Why?** The 3 correlated agents provide only 1 independent piece of evidence. If they're all wrong, that's not 3 mistakes—it's 1 systematic failure replicated 3 times.

**Formal intuition:** The effective number of independent agents is:

$$N_{\text{eff}} \approx \frac{N}{1 + (N-1)\bar{\rho}}$$

where $\bar{\rho}$ is average pairwise correlation.

- If $\bar{\rho} = 0$ (independent): $N_{\text{eff}} = N$
- If $\bar{\rho} = 0.5$: $N_{\text{eff}} \approx N/3$ (only 1/3 as effective!)
- If $\bar{\rho} = 1$ (perfect correlation): $N_{\text{eff}} = 1$ (all agents act as one)

### 3.4 How You Measured Correlation in This Project

**Step 1:** Computed pairwise error correlation matrix  
For each pair of models $(i, j)$, calculate:

$$\rho_{ij} = \frac{\sum_{t=1}^{T} (e_{i,t} - \bar{e}_i)(e_{j,t} - \bar{e}_j)}{\sqrt{\sum_{t} (e_{i,t} - \bar{e}_i)^2 \sum_{t} (e_{j,t} - \bar{e}_j)^2}}$$

**Step 2:** Visualized as heatmap  
Dark colors = high correlation (redundant)  
Light colors = low correlation (complementary)

**Step 3:** Clustered models by error patterns  
Identified which models tend to fail together vs independently

**What you found (see [Model-Comparison.ipynb](notebooks/Model-Comparison.ipynb)):**
- High-correlation pairs (r > 0.5): 35-40%
- Moderate correlation (0.2 < r < 0.5): 45-50%
- Low correlation (r < 0.2): 10-15%

**Implication:** Your ensemble has substantial redundancy. This explains why adding more models doesn't help as much as theory predicts.

**Suggested reading:**
- Zhou, Z. H. (2012). *Ensemble Methods: Foundations and Algorithms*. Chapter 4 on diversity measures.
- Kuncheva, L. I., & Whitaker, C. J. (2003). "Measures of diversity in classifier ensembles and their relationship with the ensemble accuracy." *Machine Learning* 51(2).

---

## 4. Why Majority Vote and WLC Plateau

### 4.1 Majority Voting Assumptions

**How it works:** Each agent gets 1 vote. The majority decision wins.

**Implicit assumptions:**
1. All agents are equally reliable (or we don't know who's better)
2. Agents make independent errors
3. Agents are better than random (p > 0.5)

**Why it's optimal under independence:**  
If assumptions hold, majority vote implements maximum likelihood estimation. For N independent agents with accuracy p > 0.5, accuracy increases with N.

**Why it fails under correlation:**  
If 3 agents are correlated, majority vote counts them as 3 independent votes when they're really 1. The correlated triplet can outvote 2 independent dissenting agents, even if the independents are more reliable.

### 4.2 Why WLC Helps (But Not Enough)

**Weighted Linear Combination (WLC):** Learn weights $w_i$ for each agent such that:

$$\text{Score} = \sum_{i=1}^{N} w_i \cdot d_i$$

where $d_i$ is agent $i$'s decision (0 or 1). Threshold the score to make final decision.

**Why this helps:**
- Gives higher weight to agents with historically better accuracy
- Downweights unreliable agents
- Adapts to heterogeneity (some models are better than others)

**Why it's not enough:**
- Learns weights based on *marginal* accuracy (how often each agent is right individually)
- Doesn't explicitly model correlation structure
- A highly correlated set of mediocre agents can still dominate

**Your baseline finding:** WLC improved accuracy by +3% over majority voting. This shows agent heterogeneity matters, but the improvement is modest—correlation is still causing problems.

**Analogy:**  
Imagine you're polling 10 voters about a decision:
- **Majority vote:** Everyone gets 1 vote (treats all equally)
- **WLC:** Give more votes to people who've been right before (rewards accuracy)
- **Correlation-aware:** Give 1 collective vote to a group of 5 who always agree with each other (discounts redundancy)

WLC does step 2 but not step 3.

### 4.3 Connecting to Your Baseline Findings

In [Main-Analysis.ipynb](notebooks/Main-Analysis.ipynb), you found:
- Majority voting accuracy plateaus around N=7-11 agents
- Adding more agents beyond this helps very little (+1-2%)
- WLC improves by +3%, but still shows similar plateau

**Interpretation through correlation lens:**

1. **Early gains (N=1→5):** You're adding genuinely new information. Even with some correlation, diversity helps.
2. **Plateau (N>7):** You're mostly adding correlated redundancy. New agents overlap too much with existing ensemble.
3. **WLC improvement:** Recognizes some agents are better than others, but doesn't fix the redundancy problem.

**Why this matters:** If you had perfectly independent agents, accuracy should keep improving up to N=12+. The plateau is a *signature* of correlation limiting your ensemble.

**Suggested reading:**
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*. Section 8.8 on model averaging and boosting.
- Dietterich, T. G. (2000). "Ensemble methods in machine learning." *MCS* (Multiple Classifier Systems).

---

## 5. What "Correlation Blindness" Means

### 5.1 Behavioral Definition (Not Cognitive)

**Correlation blindness** (as defined in this study) is a *behavioral pattern* where an aggregation system:

1. **Treats correlated agents as independent** when making aggregation decisions
2. **Does not adjust confidence** when redundant evidence confirms vs diverse evidence confirms
3. **Fails to improve** when explicitly informed about correlation structure

**Important:** This is NOT a claim about:
- Internal model representations
- Training procedures
- Explicit knowledge or "understanding"

It's purely about input-output behavior: Given correlation information, does the system's aggregation strategy change?

### 5.2 What Correlation-Aware vs Correlation-Blind Looks Like

**Example scenario:**
- 5 agents vote on a decision
- Agents A, B, C are highly correlated (r ≈ 0.7)
- Agents D, E are independent
- A, B, C vote "Yes"; D, E vote "No"

**Correlation-blind aggregator:**
- Majority vote: 3 vs 2 → Decision: "Yes"
- Confidence: High (3/5 majority is strong)
- Reasoning: "Most agents agree"

**Correlation-aware aggregator:**
- Effective votes: A/B/C ≈ 1.5 votes total (discounted), D = 1, E = 1 → Total: ~1.5 vs 2
- Decision: "No" (independent agents outweigh correlated cluster)
- Confidence: Moderate (evidence is less redundant than it appears)
- Reasoning: "A, B, C are redundant; I weight D and E more heavily"

### 5.3 Why This Is a New Question for LLMs

**Prior work established:**
- Humans show correlation blindness in many contexts (Sorkin & Dai, 2010; social influence literature)
- Ensemble ML systems need explicit diversity measures (Brown, 2004; Zhou, 2012)
- Optimal Bayesian aggregation requires modeling correlation (Kording & Wolpert, 2006)

**What's unknown:**
- Do LLMs, when prompted to aggregate, implicitly account for correlation?
- Can transparency (telling them about correlation) enable better aggregation?
- How does LLM aggregation compare to human aggregation and Bayesian optimal?

**Why this matters:**
- **Practically:** LLMs are increasingly used for decision support. If they're correlation-blind, they'll give overconfident recommendations when shown redundant evidence.
- **Theoretically:** Tests whether statistical reasoning about evidence combination emerges from language model training.
- **Methodologically:** Establishes whether prompting alone can induce optimal aggregation or if explicit algorithms are needed.

### 5.4 Why You're Testing This Behaviorally

You're NOT doing:
- Fine-tuning or training interventions
- Architectural modifications
- Mechanistic interpretability of internal representations

You're ONLY doing:
- Prompt engineering (transparency manipulation)
- Output measurement (accuracy, vote allocation)
- Behavioral comparison (blind vs transparent conditions)

**Advantage:** This is feasible for an undergraduate thesis (~6 weeks, ~$200 budget)  
**Limitation:** Can't make claims about *why* LLMs behave this way—only *that* they do

**Suggested reading:**
- Sorkin, R. D., & Dai, H. (2010). "Signal detection analysis of the ideal group." *Organizational Behavior and Human Decision Processes* 113(2).
- Prelec, D., Seung, H. S., & McCoy, J. (2017). "A solution to the single-question crowd wisdom problem." *Nature* 541.

---

## 6. Experimental Design Walkthrough

### 6.1 Defining Correlated vs Diverse Agent Panels

**What you do:**
- Use empirical error correlation matrix from [Model-Comparison.ipynb](notebooks/Model-Comparison.ipynb)
- Select 3-4 models with high pairwise correlation (r > 0.6) as "correlated cluster"
- Select 3-4 models with low pairwise correlation (r < 0.3) as "diverse panel"

**Why you do this:**
- Creates natural experimental conditions (high vs low correlation)
- Uses real agents, not synthetic/simulated
- Grounded in actual performance on your task

**What could go wrong:**
- **Cherry-picking:** If you choose models that happen to agree on your test trials by chance (not true correlation), the effect won't replicate
  - **Prevention:** Sample trials uniformly, stratified by difficulty
- **Confounding:** Correlated cluster might also have lower average accuracy
  - **Prevention:** Control for accuracy; compare within accuracy-matched groups if needed

**How to think about it:**
You're not manipulating correlation directly (you can't retrain the models). You're *selecting* agents with different correlation profiles and testing whether LLM aggregators respond to that difference.

### 6.2 Blind vs Transparent Aggregation Conditions

**Blind condition:**
- Prompt: "Here are 5 agent decisions..."
- No information about correlation
- Tests baseline behavior: Does LLM spontaneously discount redundancy?

**Transparent condition:**
- Prompt: "Agents A, B, C belong to same empirical error cluster (correlated on ~60% of error trials)..."
- Explicit correlation information
- Tests whether transparency enables correlation-aware aggregation

**Why both conditions:**
- **Blind:** Measures default behavior
- **Transparent:** Measures whether LLMs *can* use correlation info when provided
- **Comparison:** Transparency effect = Transparent accuracy - Blind accuracy

**What could go wrong:**
- **Demand effects:** LLM might adjust weights just because you mentioned correlation, not because it improves aggregation
  - **Prevention:** Include placebo control (see next section)
- **Phrasing effects:** Effect might depend on exact wording
  - **Prevention:** Test 2-3 transparency phrasings; ensure effect is robust

### 6.3 Placebo Transparency Controls

**Placebo condition:**
- Prompt: "All agents were evaluated on separate validation sets"
- Sounds informative but conveys no useful correlation information
- Tests whether any transparency (even non-informative) affects behavior

**Why this is critical:**
Without placebo control, you can't distinguish:
- **True correlation sensitivity:** LLM uses correlation structure to improve aggregation
- **Generic transparency effect:** LLM changes behavior whenever you add extra context

**Interpretation:**
- If Transparent > Placebo > Blind: True correlation sensitivity
- If Transparent = Placebo > Blind: Generic transparency effect (not correlation-specific)
- If Transparent = Placebo = Blind: No transparency effect at all

**What could go wrong:**
- **Placebo too obvious:** If placebo is clearly uninformative, LLM might ignore it
  - **Prevention:** Make placebo sound plausible but provide no correlation info
- **Placebo accidentally informative:** "Separate validation sets" might imply independence
  - **Mitigation:** Test multiple placebo phrasings to ensure robustness

### 6.4 Structured Output: Effective Vote Counts

**Why you need structured output:**
- Free-form text is ambiguous: "I trust Agent A more" doesn't quantify *how much*
- You need machine-scoreable metrics to analyze 1,800 responses
- Vote counts map naturally to aggregation decisions

**What you ask for:**
```json
{
  "effective_votes": {"A": 0.5, "B": 0.5, "C": 0.5, "D": 1.0, "E": 1.0},
  "decision": "Present",
  "reasoning": "...",
  "confidence": 75
}
```

**How to interpret:**
- **Uniform votes** (each agent ≈ 1): Correlation-blind behavior
- **Discounted votes** (correlated cluster < 1 per agent): Correlation-aware behavior
- **Decision consistency:** Does the decision follow from the vote allocation?

**What could go wrong:**
- **Format non-compliance:** LLM returns unstructured text instead of JSON
  - **Prevention:** Few-shot examples; explicit format instructions; parsing validation
- **Arbitrary numbers:** LLM assigns votes randomly without reasoning
  - **Prevention:** Compare vote allocation to accuracy outcomes; check for systematic patterns
- **Gaming the format:** LLM figures out it should discount and does so mechanically without understanding
  - **Detection:** Look at reasoning traces; check if vote allocation aligns with stated logic

### 6.5 Why Free-Form Explanations Are Secondary

**You include reasoning traces ("Explain your decision in 2-3 sentences") but treat them as supplementary.**

**Why?**
- **Primary metric is behavior:** Vote allocation and accuracy are objective
- **Reasoning can be post-hoc:** LLM might rationalize decisions that weren't explicitly reasoned
- **Hard to quantify:** Qualitative analysis of 1,800 text responses is time-intensive

**When reasoning is useful:**
- **Exploratory analysis:** Understand *how* LLMs are thinking about correlation
- **Failure case diagnosis:** When vote allocation looks wrong, reasoning explains why
- **Hypothesis generation:** Discover unexpected strategies that quantitative metrics miss

**What to look for in reasoning traces:**
- Do they mention correlation explicitly?
- Do they use language like "redundant," "overlapping," "independent"?
- Do they justify vote allocation with reference to correlation structure?

**Suggested reading:**
- Kleinberg, J., et al. (2018). "Human decisions and machine predictions." *QJE*.
  - Section on interpreting ML outputs vs understanding reasoning
- Lipton, Z. C. (2018). "The mythos of model interpretability." *ACM Queue*.

---

## 7. Baselines and Benchmarks

### 7.1 Why Include Majority Vote Baseline

**Majority vote** is your naïve baseline:
- Each agent gets 1 vote
- No weighting, no correlation awareness
- Simple, interpretable, widely used

**Purpose:**
- Shows what happens with *no* aggregation sophistication
- If LLM aggregation ≤ majority vote, it's performing poorly
- If LLM aggregation > majority vote, it's doing something useful

**Expected result:**
- Majority vote accuracy ≈ 65-75% (based on your baseline analysis)
- Should perform worse than correlation-aware methods when correlation is high

### 7.2 What Stacking / Logistic Regression Represents

**Stacking approach:**
1. Train logistic regression on 80% of trials (held-out from test set)
2. Input: Binary decisions from each agent
3. Output: Probability of target presence
4. Learn optimal weights $w_i$ that maximize log-likelihood

**What this represents conceptually:**
- **Data-driven oracle:** Best performance achievable by learning from historical data
- **Implicit correlation handling:** Regression learns which agent combinations are informative
- **Upper bound:** Represents achievable accuracy given your dataset

**What this is NOT:**
- **NOT Bayesian optimal:** Doesn't explicitly model correlation structure with formal probabilistic inference
- **NOT causal:** Weights are associational, not mechanistic
- **NOT interpretable:** Can't directly translate weights to "degree of correlation"

**Why you use this:**
- Feasible to compute (logistic regression is standard)
- Provides realistic performance target (not unachievable theoretical bound)
- Allows comparison: "Does LLM aggregation approach stacking performance?"

### 7.3 Why This Is an "Empirical Oracle" Not Bayesian Optimal

**Bayesian optimal aggregation** would require:
1. Exact agent accuracy parameters $p_i$
2. Full correlation matrix $\Sigma$
3. Generative model of error distributions
4. Closed-form or sampled posterior inference

**Why you don't use this:**
- **Assumption-heavy:** Real agents don't follow simple Bernoulli models
- **Computationally intensive:** Inference over 5 agents × 300 trials × 3 models = expensive
- **Not obviously better:** Stacking might actually outperform misspecified Bayesian model

**Empirical oracle (stacking) advantages:**
- **Assumption-light:** Learns directly from data
- **Fast:** Logistic regression is quick to fit
- **Interpretable:** Can inspect learned weights
- **Realistic:** Represents what's practically achievable

**How to communicate this:**
- ✓ "We compare LLM aggregation to an empirical stacking baseline"
- ✓ "Stacking represents data-driven optimal performance given our dataset"
- ✗ "We compare to Bayesian optimal aggregation"
- ✗ "Stacking is theoretically optimal"

**Suggested reading:**
- Wolpert, D. H. (1992). "Stacked generalization." *Neural Networks* 5(2).
- Breiman, L. (1996). "Stacked regressions." *Machine Learning* 24(1).

---

## 8. Interpreting Results

### 8.1 Patterns That Support Correlation Blindness

If you find:

**Primary evidence:**
1. **No transparency effect:** Transparent accuracy ≈ Blind accuracy (< 2% difference)
2. **Uniform vote allocation:** Correlated agents receive ~1 vote each (not discounted)
3. **Majority-vote-like decisions:** LLM decisions match naive majority vote >90% of time

**Supporting evidence:**
4. **No confidence adjustment:** Confidence is similar when correlated agents agree vs diverse agents agree
5. **Reasoning doesn't mention correlation:** Free-text explanations ignore correlation info even in Transparent condition
6. **Placebo = Blind:** Placebo control shows no difference from Blind (rules out generic transparency effects)

**Interpretation:**
- LLMs treat all agents as independent by default
- Transparency prompt doesn't enable correlation-aware aggregation
- Behavior resembles naive vote-counting (similar to human biases documented by Sorkin & Dai, 2010)

**Strength of conclusion depends on:**
- Effect size: Is difference truly <2% or just noisy around 3-5%?
- Consistency: Does it hold across all 3 tested LLMs?
- Robustness: Does it persist across different transparency phrasings?

### 8.2 Patterns That Falsify Correlation Blindness

If you find:

**Primary evidence:**
1. **Strong transparency effect:** Transparent accuracy > Blind by ≥5-7%
2. **Systematic vote discounting:** Correlated clusters receive significantly fewer votes per agent (e.g., 3 agents → ~1 effective vote)
3. **Approaches stacking baseline:** LLM aggregation accuracy gets within 3-5% of empirical optimal

**Supporting evidence:**
4. **Confidence calibration:** Lower confidence when correlated agents agree vs diverse agents
5. **Explicit reasoning:** Free-text mentions "redundancy," "correlation," "overlapping errors"
6. **Placebo < Transparent:** Placebo accuracy is between Blind and Transparent (shows effect is correlation-specific)

**Interpretation:**
- LLMs can recognize and discount correlated evidence when informed
- Prompting is sufficient to enable correlation-aware aggregation
- LLMs perform sophisticated evidence combination similar to Bayesian reasoning

**Follow-up questions:**
- Does this depend on model size/family?
- How much transparency detail is needed? (Can you simplify the prompt?)
- Does it generalize beyond binary decisions?

### 8.3 Interpreting Partial or Noisy Effects

**Real research is messy.** You might find:

- Transparent improves accuracy by 3-4% (not 7%, but not 0%)
- Some LLMs show effect, others don't
- Effect is stronger for high-correlation clusters, weaker for moderate correlation
- Vote discounting happens but isn't optimally calibrated

**How to interpret:**
1. **Effect size matters:** Even 3% improvement could be practically significant if it's robust
2. **Model heterogeneity is informative:** Differences between GPT-4o, Claude, Gemini tell you about generalizability
3. **Partial sensitivity is a finding:** "LLMs show emerging but incomplete correlation awareness" is a valid conclusion
4. **Check for confounds:** Could the effect be driven by prompt length? Agent label order? Task difficulty?

**Statistical considerations:**
- With 300 trials per condition, you can detect effects d ≥ 0.3
- p < 0.05 is not magic—interpret confidence intervals
- If p = 0.08, that's "suggestive but not definitive," not "failed"

**What to report:**
- ✓ Effect size with confidence intervals
- ✓ Consistency across models/conditions
- ✓ Alternative explanations you ruled out
- ✗ Binary "significant" vs "not significant" framing

### 8.4 Common Misinterpretations to Avoid

**Mistake 1: "LLMs understand correlation"**  
- **Reality:** You measured *behavior*, not understanding. LLMs might pattern-match without deep comprehension.

**Mistake 2: "Correlation blindness means LLMs are bad"**  
- **Reality:** Humans show the same bias. Optimal aggregation is hard even for expert statisticians.

**Mistake 3: "This proves training data didn't include X"**  
- **Reality:** You can't make training data claims from behavioral tests. Absence of behavior ≠ absence of knowledge.

**Mistake 4: "Stacking is optimal"**  
- **Reality:** Stacking is *empirically optimal given your dataset*. A different dataset or true Bayesian inference might do better.

**Mistake 5: "Prompting failed, so we need fine-tuning"**  
- **Reality:** Prompting limitations don't automatically imply fine-tuning will work. Could be a deeper architectural issue.

**Suggested reading:**
- Gelman, A., & Stern, H. (2006). "The difference between 'significant' and 'not significant' is not itself statistically significant." *The American Statistician* 60(4).
- Nosek, B. A., et al. (2018). "The preregistration revolution." *PNAS*.

---

## 9. What This Study Does NOT Claim

### 9.1 No Claims About Internal Representations

**You are NOT claiming:**
- LLMs have explicit "correlation detectors" in their weights
- Transformers layers compute correlation coefficients
- Attention heads encode agent relationships

**Why not:**
- You're not doing mechanistic interpretability
- Behavioral measurements are compatible with many internal mechanisms
- You don't have access to model internals (GPT-4o, Claude are closed-source)

**What you CAN say:**
- "LLM aggregation behavior is/isn't sensitive to correlation structure"
- "Transparency prompts do/don't enable better aggregation"
- "Observed behavior is consistent with correlation-blind vote-counting"

### 9.2 No Claims About Training Data

**You are NOT claiming:**
- LLMs were/weren't trained on aggregation problems
- Training data did/didn't include statistics textbooks
- Pretraining included/excluded correlation concepts

**Why not:**
- You don't have access to training data
- Behavioral outcomes underdetermine training history (many paths lead to same behavior)
- Correlation awareness could emerge from general reasoning, not specific training examples

**What you CAN say:**
- "LLMs show/don't show correlation-aware behavior when prompted"
- "Results suggest prompting alone is/isn't sufficient for optimal aggregation"

### 9.3 No Claims About Optimal Aggregation in General

**You are NOT claiming:**
- You've solved the optimal aggregation problem
- Your stacking baseline is universally best
- Results generalize to all decision-making contexts

**Scope limitations:**
- **Task-specific:** 2AFC perceptual decisions, not medical diagnosis or forecasting
- **Binary decisions:** Doesn't address confidence-weighted aggregation
- **Specific agents:** Results for GPT-4o/Claude/Gemini, not all LLMs
- **Empirical correlation:** Not causal/mechanistic correlation

**What you CAN say:**
- "In this task, with these agents, we observed..."
- "Results suggest correlation matters for LLM aggregation in this context"
- "Follow-up work should test generalization to..."

### 9.4 No Claims About AGI, "Understanding," or Consciousness

**You are NOT claiming:**
- LLMs "truly understand" aggregation
- Correlation blindness reveals deep cognitive limitations
- This tells us about AI consciousness or reasoning

**Why this matters:**
- Your study is behavioral/functional, not philosophical
- Anthropomorphic language undermines scientific credibility
- You're measuring input-output patterns, not mental states

**How to frame findings:**
- ✓ "LLM aggregation behavior exhibits/lacks correlation sensitivity"
- ✓ "Prompting interventions do/don't improve aggregation performance"
- ✗ "LLMs understand/don't understand correlation"
- ✗ "LLMs think/reason/believe..."

---

## 10. How This Fits Into a Larger Research Arc

### 10.1 Building on the Baseline

**Phase 1 (Complete):** Baseline analysis
- Characterized human & LLM performance
- Identified ensemble plateau
- Computed error correlation structure
- Established WLC improves modestly

**Phase 2 (This study):** Correlation blindness
- Tests whether LLMs recognize correlation
- Measures transparency effects
- Compares to empirical optimal

**Logical connection:**
Baseline revealed correlation as limiting factor → Next study tests if aggregators account for it

### 10.2 Follow-Up Questions This Enables

**If LLMs are correlation-blind:**
1. Can fine-tuning on aggregation tasks teach correlation awareness?
2. Do explicit preprocessing modules (cluster detection) help?
3. How do LLMs compare to humans on same task?

**If LLMs are correlation-aware:**
1. What's the minimal transparency needed? (Can you simplify prompts?)
2. Does it generalize to other tasks (forecasting, diagnosis)?
3. Can LLMs *discover* correlation from data without being told?

**If results are mixed:**
1. Which model architectures show sensitivity?
2. What training characteristics predict correlation awareness?
3. Can you combine correlation-blind and correlation-aware models?

### 10.3 Why This Scope Is Appropriate for Undergraduate Thesis

**Feasibility:**
- **Time:** 6 weeks (1 pilot, 2 data collection, 2 analysis, 1 writing)
- **Budget:** $175-225 (well under $700 limit)
- **Technical complexity:** Prompting + logistic regression (no custom training)
- **Infrastructure:** Uses existing dataset and code pipeline

**Scientific value:**
- **Novel question:** Correlation blindness in LLM aggregators is unexplored
- **Clear hypothesis:** Testable with quantitative metrics
- **Real-world relevance:** Informs AI decision-support system design

**Learning outcomes:**
- Experimental design (conditions, controls, confounds)
- Statistical reasoning (power analysis, effect sizes, interpretation)
- Scientific writing (grounding claims, avoiding overclaiming)
- Research taste (scoping questions, managing uncertainty)

**What makes a good undergraduate thesis:**
- ✓ Focused question (not "solve aggregation")
- ✓ Feasible methods (not "train new models from scratch")
- ✓ Clear contribution (not "replicate existing work")
- ✓ Realistic scope (not "10 studies in 5 months")

### 10.4 Publication and Career Trajectory

**Realistic publication targets:**
- **Workshops:** NeurIPS/ICML Collective Intelligence, Human-AI Interaction
- **Conferences:** Cognitive Science Society, AI & Society
- **Journals:** (after thesis defense) Decision Support Systems, AI & Ethics

**What this demonstrates for graduate school applications:**
- Independent research from dataset → hypothesis → execution → writing
- Understanding of statistical foundations (SDT, correlation, ensemble learning)
- Ability to scope tractable questions
- Scientific communication skills

**Beyond this thesis:**
- Could extend to multi-agent systems, human-AI teams, organizational decision-making
- Connects to AI safety (overconfidence from redundant evidence)
- Bridges ML, psychology, and decision theory

---

## 11. Recommended Readings by Topic

### Foundations: Collective Intelligence
- Surowiecki, J. (2004). *The Wisdom of Crowds*. [Chapters 1-3]
- Condorcet, J. A. N. (1785). *Essay on the Application of Analysis to the Probability of Majority Decisions*.
- Hong, L., & Page, S. E. (2004). "Groups of diverse problem solvers can outperform groups of high-ability problem solvers." *PNAS* 101(46).

### Ensemble Learning & Diversity
- Zhou, Z. H. (2012). *Ensemble Methods: Foundations and Algorithms*. [Chapters 1, 4]
- Brown, G. (2004). "Diversity in neural networks for classification." *Machine Learning* 57(3).
- Kuncheva, L. I., & Whitaker, C. J. (2003). "Measures of diversity in classifier ensembles." *Machine Learning* 51(2).

### Bayesian Decision Theory
- Kording, K. P., & Wolpert, D. M. (2006). "Bayesian decision theory in neuroscience." *Trends in Cognitive Sciences* 10(12).
- Sorkin, R. D., & Dai, H. (2010). "Signal detection analysis of the ideal group." *Organizational Behavior and Human Decision Processes* 113(2).

### Aggregation Methods
- Wolpert, D. H. (1992). "Stacked generalization." *Neural Networks* 5(2).
- Prelec, D., Seung, H. S., & McCoy, J. (2017). "A solution to the single-question crowd wisdom problem." *Nature* 541.

### LLM Evaluation & Reasoning
- Lipton, Z. C. (2018). "The mythos of model interpretability." *ACM Queue* 16(3).
- Kleinberg, J., et al. (2018). "Human decisions and machine predictions." *QJE* 133(1).

### Statistical Interpretation
- Gelman, A., & Stern, H. (2006). "The difference between 'significant' and 'not significant' is not itself statistically significant." *The American Statistician* 60(4).
- Cumming, G. (2014). "The new statistics: Why and how." *Psychological Science* 25(1).

---

## 12. Final Thoughts: Thinking Like a Researcher

### 12.1 What Makes This a Research Question (Not Just Data Analysis)

**It's a research question because:**
- There's genuine uncertainty (no one knows the answer)
- It's theoretically motivated (connects to broader understanding of collective intelligence)
- Results inform future work (regardless of which hypothesis is supported)
- It requires careful experimental design (not just descriptive statistics)

**It's NOT just data analysis because:**
- You're testing a hypothesis, not just reporting numbers
- You're manipulating conditions (Blind vs Transparent)
- You're comparing to meaningful baselines (stacking, majority vote)
- You're interpreting mechanisms (correlation awareness vs blindness)

### 12.2 How to Maintain Scientific Integrity

**Preregister when possible:**
- Write down hypotheses before running analysis
- Commit to analysis plan (primary metrics, sample size, exclusion criteria)
- Distinguish confirmatory tests from exploratory analyses

**Report everything:**
- Include results that don't fit your story
- Report effect sizes, not just p-values
- Acknowledge limitations and alternative explanations

**Avoid HARKing** (Hypothesizing After Results Known):
- If you discover something unexpected, frame it as exploratory
- Don't pretend you predicted post-hoc observations
- Separate "predicted" from "discovered" findings

**Be transparent about decisions:**
- Why did you choose these agent groups?
- Why 300 trials not 200 or 500?
- How did you handle malformed LLM outputs?

### 12.3 When to Ask for Help

**You should ask your advisor/mentor when:**
- You're unsure how to interpret an unexpected result
- You're deciding between multiple analysis approaches
- You're stuck on a confound you can't rule out
- You're writing up and want feedback on claims

**You should figure out yourself when:**
- Implementing standard methods (logistic regression, t-tests)
- Debugging code or data formatting
- Organizing files and documentation
- Making plots and tables

**The line:** If it affects the validity of your scientific conclusions, ask. If it's technical execution, try first.

### 12.4 This Document Is a Living Resource

**How to use this:**
- Read it before starting experiments (understand the "why")
- Reference it during analysis (check interpretations)
- Cite it in your thesis (ground design decisions)
- Update it if you discover something that changes your understanding

**This is not scripture:**
- If you find a better way to do something, do it
- If you disagree with an interpretation, think through why
- If new information changes the framing, revise your understanding

**Good researchers:**
- Question assumptions (including their own)
- Update beliefs based on evidence
- Communicate uncertainty honestly
- Build on prior work while pushing boundaries

---

**You're ready.** This study is well-scoped, grounded in real data, and addresses a meaningful question. Execute carefully, interpret honestly, and write clearly. Good luck.

**— January 2026**
