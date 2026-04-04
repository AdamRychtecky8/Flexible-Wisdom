# Research Context

## Background

This project replicates and extends Juni & Eckstein (2015), which established that human groups improve collective decision accuracy through majority voting on perceptual tasks. This work asks whether LLM ensembles show the same pattern — and if so, whether the same limiting factors apply.

The Condorcet Jury Theorem (1785) predicts that majority voting accuracy approaches 100% as group size N increases, under the assumption that agents make *independent* errors. In practice, agents trained on similar data or exposed to similar biases make correlated errors — they fail on the same trials — which means the effective group size is far smaller than the nominal group size. Standard aggregation methods (majority voting, simple averaging) do not account for this.

## Central Finding

Both human and LLM ensembles plateau well below the Condorcet prediction. In this dataset, ensemble accuracy saturates around n ≈ 7 agents, after which adding more agents contributes only ~1–2% additional gain. The mechanistic explanation — high pairwise error correlation across LLM agents (35–40% of pairs with r > 0.5) — has direct implications for how multi-agent AI systems should be designed and evaluated. An ensemble of 12 highly correlated models provides far less independent evidence than 12 agents, and naive aggregation treats their agreement as 12 independent confirmations rather than a single correlated signal.

## Proposed Phase 2: Correlation Blindness

The proposed follow-up study tests whether LLMs — when used as *meta-level aggregators* — can detect and compensate for this correlation. Specifically: when explicitly informed that a subset of agents share correlated error patterns, do LLMs adjust their vote allocation to discount redundant agents? Or do they exhibit "correlation blindness" — treating correlated agreement as if it were independent?

This question has direct relevance to:
- **Ensemble learning:** Whether LLM-based aggregation can implement diversity-aware combination without explicit algorithmic design
- **Mixture-of-experts architectures:** When routing decisions across specialized models, is the router sensitive to error correlation between experts?
- **Human-AI teaming:** Do humans + LLMs compound each other's biases when both are correlation-blind, or does diversity of error type preserve ensemble quality?
- **AI advisory systems:** When an AI system aggregates multiple AI opinions before presenting a recommendation, does it appropriately weight redundant evidence?

## Theoretical Grounding

**Condorcet Jury Theorem (1785):** Majority voting converges to truth as N → ∞ under independence. Violated when errors are correlated.

**Brown (2004):** Correlated errors in neural network ensembles eliminate diversity benefits entirely. The ensemble behaves as a single agent when correlation is high.

**Zhou (2012):** Ensemble accuracy is bounded by the correlation structure of agent errors. Adding correlated agents yields diminishing returns bounded by effective group size k < N.

**Sorkin & Dai (2010):** Human groups fail to discount redundant information from correlated informants — a psychological bias that mirrors what we hypothesize LLMs may also exhibit.

**Kording & Wolpert (2006):** Bayesian optimal aggregation requires downweighting correlated evidence. This is the normative benchmark against which both human and LLM behavior should be compared.

## Positioning

Most ensemble research in ML enforces or assumes agent independence (e.g., bagging, random forests, dropout ensembles). Most LLM reasoning research focuses on single-agent accuracy. This project sits at the intersection: using a large-scale human + LLM dataset to measure whether independence assumptions hold empirically, and whether LLMs can reason about their own violation when acting as aggregators.

The dataset is unusual in that every agent — human and LLM — sees identical stimuli under identical conditions, with known ground truth, enabling exact error correlation measurement rather than proxy metrics.

---

**Advisor:** [Adam to fill in]  
**Lab:** Vision & Image Understanding Lab, UCSB  
**Phase 1 complete:** January 2026  
**Phase 2 proposed:** February–March 2026  
**Thesis target:** Spring 2026
