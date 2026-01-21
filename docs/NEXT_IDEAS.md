# Next Ideas: Strategic LLM Research on Correlation Blindness

**Date:** January 20, 2026  
**Focus:** How to research LLM reasoning and detect systematic biases in ensemble aggregation  
**Target:** Mechanistic interpretability through structured prompting experiments  

---

## Overview

Given the **correlation blindness research direction** (established in FUTURE_DIRECTIONS.md), this document outlines a strategic approach to understanding **how LLMs function when aggregating decisions from correlated agents**.

The key insight: **Use structured prompting as a window into LLM reasoning**, not just to measure accuracy.

---

## 1. High-Level Strategy

### Core Principle

Transform a simple "measure LLM accuracy" study into a **mechanistic interpretability study** that reveals:
- Whether LLMs recognize correlation
- What reasoning heuristics they actually use
- How transparency/hints affect their decision-making
- Where they systematically fail vs succeed

### Competitive Advantage

Most LLM research uses **synthetic scenarios**. Your advantage:
- ✅ Real agent decisions from 507k trials
- ✅ Measured correlations (35–40% redundancy quantified)
- ✅ Empirical ground truth (know who actually performed best)
- ✅ Bayesian optimal baseline (compare LLM to theory)

This makes findings **more credible and publishable**.

---

## 2. Methodology: Tiered Prompting Strategy

### Why Tiers Matter

Instead of one-off prompts, design a **progression that reveals reasoning**:

#### **Tier 1: Minimal (Baseline Blindness Test)**
```
Prompt: "Here are 5 agent decisions on a task. 
         Which agent's decision should we trust most?"

Agent A: "Target present" (confidence: 0.85)
Agent B: "Target present" (confidence: 0.82)
Agent C: "Target absent" (confidence: 0.70)
Agent D: "Target present" (confidence: 0.88)
Agent E: "Target absent" (confidence: 0.75)

What's your choice and why?
```

**Measure:**
- Which agent does LLM pick?
- Confidence in choice
- Does LLM mention correlation or similarity? (it shouldn't at this stage)
- Is reasoning purely confidence-based?

**Hypothesis:** If LLM is correlation-blind, it will pick Agent D (highest confidence) without noting that A, B, D are probably correlated.

---

#### **Tier 2: Forced Reflection (Revealing Heuristics)**
```
Prompt: "Here are 5 agent decisions. Analyze each:

Agent A: "Target present" (confidence: 0.85)
Agent B: "Target present" (confidence: 0.82)  [Note: A & B trained on same data]
Agent C: "Target absent" (confidence: 0.70)
Agent D: "Target present" (confidence: 0.88)
Agent E: "Target absent" (confidence: 0.75)

Please answer:
1. Which agents seem most reliable?
2. Do any agents seem similar or correlated?
3. If forced to trust ONE agent, who would it be? Why?
4. How confident are you in this choice?"
```

**Measure:**
- Does LLM now identify the correlation hint?
- Does it change its choice compared to Tier 1?
- What reasoning is given?
- Extract: confidence-based vs diversity-based vs correlation-aware reasoning

**Key difference from Tier 1:** We're asking LLM to *reflect* on correlation explicitly.

---

#### **Tier 3: Bayesian Scaffolding (Can It Learn?)**
```
Prompt: "Here are 5 agent decisions.

[Same scenario as above]

Important context: Agents A and B were trained on the same dataset 
and make correlated errors. When A is right, B is usually right too. 
When A is wrong, B is usually wrong too.

Given this, which agent should we trust? Explain your reasoning."
```

**Measure:**
- Can LLM adjust when correlation is *explicitly explained*?
- Does it downweight A and B in favor of diverse agents?
- How much scaffolding is needed?

**Expected finding:** If correlation-blindness is real, LLM should improve with explicit hints. If LLM was already correlation-aware (Tier 2), no change expected.

---

#### **Tier 4: Reasoning Extraction (Meta-Analysis)**
```
Prompt: "Explain your decision-making process step-by-step:

1. For each agent, estimate how reliable they are. Why?
2. If you noticed any patterns (e.g., some agents always agree), 
   what does that tell you?
3. How confident are you? What would change your mind?
4. Describe the exact reasoning you used to pick the agent you chose."
```

**Measure:**
- Extract explicit reasoning from natural language
- Classify into categories: confidence, diversity, correlation, consensus, other
- Identify which heuristics LLM actually uses
- Check consistency with Tier 1–3 choices

**Expected finding:** If LLM uses implicit heuristics (e.g., always picks highest confidence), this should reveal it.

---

### Why This Progression Works

| Tier | Reveals | Design |
|------|---------|--------|
| 1 | Baseline behavior under minimal info | No hints about correlation |
| 2 | Whether LLM notices correlation naturally | Asks to reflect; mentions correlation in scenario |
| 3 | Whether LLM can *learn* when told | Explicit scaffolding about correlation |
| 4 | What heuristics actually drive choices | Forces articulation of reasoning |

If you see this pattern:
- Tier 1: Wrong choice (picks correlated agent)
- Tier 2: Same wrong choice (doesn't notice even when asked)
- Tier 3: Corrects choice (but only with explicit hint)
- Tier 4: Admits using confidence heuristic despite correlation

→ **Strong evidence of correlation blindness + specific mechanism.**

---

## 3. Interpretability: Extract Reasoning, Don't Just Count Accuracy

### Standard (Shallow) Approach ❌

```
for scenario in scenarios:
    response = llm.prompt(scenario)
    choice = parse_choice(response)
    accuracy = (choice == ground_truth_best_agent)
    results.append({"scenario": scenario, "accuracy": accuracy})
```

Problem: You know the *outcome* but not the *reasoning*. Can't distinguish:
- Did LLM not notice correlation?
- Did LLM notice but ignore it?
- Does LLM use a different reasoning system altogether?

### Better Approach ✅

```python
# 1. Parse reasoning text into categories
reasoning_patterns = {
    "confidence_only": r"(highest|strongest|best confidence|most confident)",
    "diversity_aware": r"(different|diverse|unique|complementary|varied)",
    "correlation_aware": r"(similar|correlated|redundant|same training|same error)",
    "consensus": r"(agree|consensus|majority|agreement)",
    "independence": r"(independent|separate|uncorrelated)",
}

# 2. Classify response
def classify_reasoning(response_text):
    categories_found = {}
    for category, pattern in reasoning_patterns.items():
        if re.search(pattern, response_text.lower()):
            categories_found[category] = True
    return categories_found

# 3. Log everything
experiment_result = {
    "trial_id": "scenario_042",
    "llm_model": "gpt-4o",
    "tier": 2,
    "scenario_type": "high_correlation",
    "agent_correlations_in_scenario": {"A-B": 0.78, "C-D": 0.12},
    
    # Raw data
    "llm_response": full_response_text,
    "llm_choice": "A",
    "llm_confidence": 0.72,
    
    # Extracted reasoning
    "reasoning_categories": ["confidence_only"],  # Did NOT mention diversity
    "mentions_correlation": False,
    
    # Ground truth comparisons
    "empirical_best_agent": "E",
    "llm_was_correct": False,
    "bayesian_optimal_choice": "E",
    "llm_vs_bayesian": "suboptimal",
}
```

**Why this matters:**
- You can correlate *reasoning patterns* with *accuracy*
- You can test: "When LLM uses diversity heuristic vs confidence heuristic, which performs better?"
- You can see: "LLM never mentions correlation across 200 trials" → evidence of blindness

---

## 4. Comparative Baselines: How Do We Know It's a Limitation?

### You Need Three Comparison Points

#### **Baseline 1: Empirical Correctness**

For each scenario, measure:
```python
{
    "empirical_best_agent": "E",  # Actually made best decision
    "llm_picked_agent": "A",
    "llm_was_correct": False,
    
    # Failure analysis
    "why_llm_wrong": "Picked high-confidence but correlated agent",
    "llm_confidence_in_choice": 0.72,
    "optimal_confidence_should_have_been": 0.85,
}
```

**Key insight:** When LLM fails, is it because:
- It didn't notice correlation?
- It noticed but underweighted diversity?
- It used a wrong heuristic?

---

#### **Baseline 2: Bayesian Optimal**

Given *measured* correlations and accuracies, compute theoretical optimal:

```python
# Pseudo-code
def bayesian_optimal_weight(agent_accuracies, agent_correlations):
    """
    Given agent accuracies and measured error correlations,
    what weights maximize expected performance?
    """
    # Solve: w* = argmax E[accuracy | w, correlations]
    # Using your measured correlations from the dataset!
    return optimal_weights

for scenario in scenarios:
    optimal_weights = bayesian_optimal_weight(accuracies, correlations)
    optimal_choice = agents[argmax(optimal_weights)]
    
    llm_choice_quality = compare_to_optimal(llm_choice, optimal_choice)
```

**Key insight:** If LLM consistently underweights diversity:
- Bayesian optimal might give equal weight to A, B, C
- LLM always picks A (highest confidence, but correlated with B, C)
- Quantify the gap: "LLM suboptimal by 3.2% due to correlation blindness"

---

#### **Baseline 3: Human Group Judgment**

Ask humans: "Which agent should we trust?"
```python
# Human control condition
human_choices = survey_humans(scenarios)

compare_llm_to_human = {
    "scenarios_llm_and_human_agree": 0.68,
    "scenarios_llm_better_than_human": 0.15,
    "scenarios_human_better_than_llm": 0.17,
    
    # Key: Do humans notice correlation better?
    "correlation_scenarios_human_accuracy": 0.82,
    "correlation_scenarios_llm_accuracy": 0.65,
}
```

**Key insight:** If humans outperform LLMs on correlation scenarios specifically, that's strong evidence LLMs have a systematic bias.

---

## 5. Data Collection: Structured Experiment Log

### What to Record for Every Trial

```python
experiment_log_entry = {
    # Identifiers
    "trial_id": "cb_001",
    "timestamp": "2026-01-20T14:32:00",
    "llm_model": "gpt-4o",
    "tier": 2,
    
    # Scenario properties
    "scenario_type": "high_correlation",
    "n_agents": 5,
    "task_difficulty": "hard",  # 50_50 condition
    
    # Agent correlations (use YOUR measured values from dataset)
    "agent_correlations": {
        "A-B": 0.78,
        "A-C": 0.15,
        "A-D": 0.22,
        "A-E": -0.05,
        "B-C": 0.12,
        "B-D": 0.81,
        "B-E": 0.10,
        "C-D": 0.18,
        "C-E": 0.92,  # E correlated with C
        "D-E": 0.20,
    },
    
    # Agent properties
    "agent_accuracies": [0.82, 0.80, 0.55, 0.78, 0.71],
    "agent_confidences": [0.85, 0.82, 0.70, 0.88, 0.75],
    
    # LLM Response
    "llm_choice": "D",
    "llm_confidence": 0.72,
    "llm_reasoning_raw": "Agent D has the highest confidence at 0.88, suggesting strongest conviction...",
    
    # Extracted reasoning
    "reasoning_categories": ["confidence_only"],
    "mentions_correlation": False,
    "mentions_diversity": False,
    "mentions_independence": False,
    "reasoning_quality": "simple",
    
    # Ground truth
    "empirical_best_agent": "B",  # B actually performed best
    "llm_was_correct": False,
    
    # Bayesian comparison
    "bayesian_optimal_choice": "B",
    "llm_vs_bayesian_gap": -0.08,  # LLM 8% worse than optimal
    "reason_for_gap": "ignored_correlation_between_D_and_A",
    
    # Human comparison
    "human_choice": "B",
    "human_agrees_with_llm": False,
    
    # Meta
    "scenario_id_from_real_data": 12345,  # Link back to your 507k trials
}
```

**Why this structure:**
- Each trial is fully documented
- Can filter/analyze by any property
- Can correlate reasoning patterns with accuracy
- Traceable to original dataset

---

## 6. Analysis Strategy: What Gets Published

### Focus on These Findings (Publish-Worthy)

#### **Finding 1: Correlation Blindness Quantification**
```
Metric: "Correlation Weighting Index"
  - Measure: correlation(llm_weights, measured_correlations)
  - Expected under blindness: ≈ 0 (no relationship)
  - Expected under awareness: > 0.5 (weights account for correlation)
  
Result: 
  "LLMs show CWI = 0.08 (blind to correlation)
   Humans show CWI = 0.64 (aware)
   Bayesian optimal = 1.0 (perfect)"
```

#### **Finding 2: Transparency Effect**
```
Tier progression effect:
  - Tier 1 (blind): 65% accuracy on high-correlation scenarios
  - Tier 2 (reflect): 67% accuracy (modest improvement)
  - Tier 3 (explicit hint): 82% accuracy (major improvement)
  
Interpretation:
  "Transparent information about correlation substantially improves LLM 
   aggregation, suggesting correlation blindness is remediable."
```

#### **Finding 3: Reasoning Pattern Classification**
```
Heuristic usage:
  - Confidence-only: 78% of trials
  - Diversity-aware: 8% of trials
  - Correlation-aware: 2% of trials
  - Consensus: 12% of trials

Accuracy by heuristic:
  - Confidence-only: 68%
  - Diversity-aware: 84%
  - Correlation-aware: 91%
  - Consensus: 72%

Interpretation:
  "LLMs predominantly use confidence heuristic, which underperforms
   diversity and correlation-aware strategies."
```

#### **Finding 4: Model-Specific Patterns**
```
Comparison across 5 models:
  - GPT-4o: 65% accuracy, 78% confidence-only heuristic
  - Claude-3.5: 72% accuracy, 45% confidence-only heuristic
  - Gemini-2.0: 69% accuracy, 82% confidence-only heuristic
  - Llama-2: 58% accuracy, 90% confidence-only heuristic
  - Mixtral: 68% accuracy, 75% confidence-only heuristic

Interpretation:
  "Correlation blindness varies by model; larger models (GPT, Claude)
   show more awareness, but all remain suboptimal."
```

---

## 7. Recommended Experiment Design

### Phase 1: Pilot (1 Week)
**Goal:** Validate methods before full study

```
Design:
  - 10 scenarios × 3 tiers × 2 models = 60 trials
  - Scenarios: Mix of high/low correlation, easy/hard tasks
  - Models: GPT-4o, Gemini-2.0

Measures:
  - Can we reliably extract reasoning? (manual review 100%)
  - Does tier progression show expected pattern?
  - Are costs reasonable? (~$10-15)

Decision point:
  - If extraction works & patterns clear: proceed to full study
  - If unclear: refine prompts/classification before scaling
```

### Phase 2: Full Study (2-3 Weeks)
**Goal:** Collect sufficient data for statistical significance

```
Design:
  - 50 scenarios × 3 tiers × 5 models = 750 trials
  - Scenarios: Systematically vary correlation level, task difficulty
  - Models: GPT-4o, Claude-3.5, Gemini-2.0, Llama-2, Mixtral
  - Balance: 50% high-correlation, 50% low-correlation scenarios

Measures:
  - All metrics from section 6
  - Cost: $150-200

Output:
  - results_df.csv with all trial data
  - Ready for analysis
```

### Phase 3: Analysis & Interpretation (1-1.5 Weeks)
**Goal:** Extract findings from data

```
Tasks:
  - Statistical tests: correlation blindness significant? (correlation test)
  - Effect sizes: how much does blindness matter? (Cohen's d)
  - Qualitative: thematic coding of reasoning patterns
  - Visualization: plots showing tier effects, model comparisons
  - Comparison: LLM vs human vs Bayesian optimal

Output:
  - Analysis notebook with reproducible code
  - Figures for paper
  - Summary statistics table
```

### Phase 4: Writing (1.5 Weeks)
**Goal:** Publication-ready paper

```
Structure:
  - Introduction: Why correlation matters in AI systems
  - Methods: Tiered prompting, reasoning extraction
  - Results: Correlation blindness findings
  - Discussion: Implications for AI alignment & ensemble design
  - Conclusion: Future directions

Sections:
  - Main findings (2-3 pages)
  - Detailed methods (1-2 pages)
  - Results & figures (2-3 pages)
  - References & appendix (1-2 pages)

Length: 8-10 pages (target: Cognitive Science, Frontiers AI, or NeurIPS workshop)
```

---

## 8. Tools & Infrastructure

### Build Minimally (Use What You Have)

**Existing assets:**
- ✅ Data: 507k trials, measured correlations
- ✅ Code: src/data_loaders.py, modular pipeline
- ✅ Infrastructure: notebooks, outputs, git setup

**New modules to add:**

```python
# Create: src/llm_prompting.py
class CorrelationBlindnessStudy:
    """Run tiered prompting experiments on correlation blindness."""
    
    def __init__(self, api_keys_config):
        self.models = {
            "gpt-4o": OpenAI(api_key=api_keys_config["openai"]),
            "claude": Anthropic(api_key=api_keys_config["anthropic"]),
            "gemini": Anthropic(api_key=api_keys_config["google"]),  # or appropriate client
            # ... etc
        }
    
    def generate_scenario(self, agent_data, correlation_level="high"):
        """
        Create a scenario using YOUR measured correlations & agents.
        
        Args:
            agent_data: dict with correlations, accuracies from dataset
            correlation_level: "high" (>0.6) or "low" (<0.3)
        
        Returns:
            scenario_text: formatted prompt scenario
        """
        pass
    
    def prompt_tier(self, scenario_text, tier=1):
        """Generate prompt for given tier (1-4)."""
        pass
    
    def prompt_llm(self, model_name, scenario_text, tier):
        """Send prompt to LLM, get response."""
        pass
    
    def extract_reasoning(self, response_text):
        """Parse response into structured reasoning categories."""
        pass
    
    def evaluate_trial(self, llm_choice, empirical_best, bayesian_optimal):
        """Compare LLM choice to baselines."""
        pass
    
    def log_trial(self, experiment_result):
        """Record full trial data."""
        pass
    
    def run_full_study(self, n_scenarios=50, tiers=[1,2,3,4], models=None):
        """Run complete experiment."""
        results = []
        for scenario in scenarios:
            for tier in tiers:
                for model in models:
                    result = self.prompt_llm(model, scenario, tier)
                    result = self.extract_reasoning(result)
                    result = self.evaluate_trial(result)
                    self.log_trial(result)
                    results.append(result)
        return pd.DataFrame(results)
```

**Notebooks to create:**

```
notebooks/
├── Correlation-Blindness-Setup.ipynb      # Generate scenarios from YOUR data
├── Correlation-Blindness-Prompting.ipynb  # Run all tiers × models
├── Correlation-Blindness-Analysis.ipynb   # Extract findings
└── Correlation-Blindness-Visualization.ipynb  # Create paper figures
```

**Output structure:**
```
outputs/
├── correlation-blindness-raw-responses/   # Raw LLM text responses
├── correlation-blindness-results.csv      # Structured trial data
├── correlation-blindness-analysis.pkl     # Analysis objects (stats, classifications)
└── correlation-blindness-figures/         # Plots for paper
```

---

## 9. LLM Selection: Which Models to Test

### Test at Least 5 Models

| Model | Reasoning | Cost | Speed | Why |
|-------|-----------|------|-------|-----|
| **GPT-4o** | Excellent | $$$ | Medium | SOTA reasoning, strong baseline |
| **Claude 3.5** | Excellent | $$$ | Medium | Great at explaining reasoning |
| **Gemini 2.0** | Good | $$ | Fast | Different architecture |
| **Llama 2** | Fair | $ | Fast | Open-source, lower capability |
| **Mixtral** | Good | $$ | Fast | MoE, different design |

### Why Diversity Matters

- **If all models show correlation blindness** → Fundamental LLM property (most publishable)
- **If only some models do** → Model-specific bias (still interesting)
- **If capability correlates with blindness** → "Larger models better at correlation detection" (novel finding)

### Cost Breakdown (5 models)

```
Full study: 750 trials
Cost per model: 150 trials × avg_cost_per_token

GPT-4o (expensive): 150 × $0.003 = $450 ❌ Too much
Reduced: 50 trials × $0.003 = $150
Claude: 50 × $0.003 = $150
Gemini: 50 × $0.002 = $100
Llama: 50 × $0.001 = $50
Mixtral: 50 × $0.002 = $100

Total: ~$550
Budget: $200-300 ✓ Fits if you prioritize cheaper models
Alt budget: $200-300 = focus on 2-3 models (GPT-4o, Claude, Gemini)
```

**Recommendation:** Start with GPT-4o (strongest reasoning), Gemini (different arch), Llama (open-source). Add Claude & Mixtral if budget allows.

---

## 10. Key Competitive Advantage: Use Your Real Data

### Most LLM Studies (❌ Shallow)

```
Create synthetic scenarios:
  - "Imagine 5 agents where 3 are correlated..."
  - Problem: Artificial, easy to game
  - Problem: No ground truth
  - Problem: Optimal solution unclear
```

### Your Study (✅ Rigorous)

```
Use REAL agent decisions from 507k trials:
  - Agent A, B, C = actual model responses
  - Correlations = measured from your dataset (35-40% redundancy real)
  - Ground truth = actual empirical performance (who was right?)
  - Bayesian optimal = computed from YOUR measured correlations
  
Result:
  - Scenarios are realistic
  - Solutions are grounded in data
  - Findings transfer to real-world ensemble systems
```

**This is why your study is publishable:**
You're not measuring "can LLM reason about abstract correlation?" (boring).
You're measuring "does LLM properly aggregate our real model ensemble?" (concrete, useful).

---

## 11. Timeline & Budget Summary

### Full Study Timeline

| Phase | Duration | Tasks | Cost |
|-------|----------|-------|------|
| **Planning** | 3 days | Prompt design, scenario generation, pilot | $0 |
| **Pilot** | 1 week | 60 trials (2 models), validate extraction | $15 |
| **Full Study** | 2 weeks | 750 trials (5 models), data collection | $200-300 |
| **Analysis** | 1 week | Stats, visualization, thematic coding | $0 |
| **Writing** | 1 week | Draft paper, figures, submission prep | $0 |
| **Buffer** | — | Re-runs, edge cases, validation | $100 |
| **TOTAL** | ~6 weeks | Complete study + publication-ready paper | **~$300-400** |

### Milestone Checkpoints

```
✓ Week 1 end: Pilot complete, methods validated
✓ Week 3 end: Full data collection complete
✓ Week 4 end: Analysis finished, findings clear
✓ Week 5 end: First draft written
✓ Week 6 end: Ready for advisor review / conference submission
```

---

## 12. Research Questions Checklist

Before you start, make sure these are clear:

- [ ] **Q1: Existence.** Do LLMs show correlation blindness on our benchmark?
- [ ] **Q2: Mechanism.** What heuristics do they use instead? (confidence, consensus, recency)
- [ ] **Q3: Remediability.** Can transparency/hints fix it? (How much scaffolding needed?)
- [ ] **Q4: Universality.** Is this all LLMs or model-specific?
- [ ] **Q5: Severity.** How much does it hurt performance? (quantify the cost)
- [ ] **Q6: Reasoning.** Do LLMs ever explicitly mention correlation? (extract examples)

If you can answer 4-5 of these with novel findings → **Publishable.**

---

## 13. Next Steps (Action Plan)

### Immediate (This Week)

- [ ] Review this document with advisor
- [ ] Finalize LLM selection (which 3-5 models?)
- [ ] Decide on API budget ($200-300 or $500+?)
- [ ] Pick target venue (Cognitive Science? Frontiers? NeurIPS workshop?)

### Short-term (Week 1-2)

- [ ] Create `src/llm_prompting.py` with scenario generation & tier prompts
- [ ] Generate 50 scenarios from your real data correlations
- [ ] Run 60-trial pilot with GPT-4o + Gemini
- [ ] Validate reasoning extraction (manual review)

### Medium-term (Week 2-4)

- [ ] Scale to 750 trials × 5 models
- [ ] Collect all data + reasoning extractions
- [ ] Analyze findings (stats, visualizations)
- [ ] Draft paper

### Long-term (Week 4-6+)

- [ ] Get advisor feedback
- [ ] Submit to target venue
- [ ] Build on findings (reliability learning, rule emergence)

---

## Conclusion

**Core Insight:** You have a rare opportunity to study LLM reasoning with *real data* and *measured ground truth*. This makes your study more credible than typical prompting research.

**Key Success Factor:** Don't just measure accuracy. **Extract and analyze reasoning patterns**. That's where the novel insight lives.

**Publication Potential:** A focused study on "How do LLMs handle correlated agents in ensemble aggregation?" is novel, concrete, and has immediate real-world implications for AI systems.

**Timeline:** 6 weeks from start to publication-ready paper, $300-400 budget.

Ready to build the prompting infrastructure?
