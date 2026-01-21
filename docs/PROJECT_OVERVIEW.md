# AGENT_BRIEF — Flexible Wisdom (Undergrad Research Project)

## What this is
This is an undergraduate research project in the UCSB Vision & Image Understanding Lab, inspired by “Wisdom of Crowds.”
The project is meant to be *fun but real*: build and evaluate agent-aggregation methods (human + AI agents) using an existing dataset.

## Core objective (do not change)
Use my existing dataset of agent decisions to study and build meta-aggregation methods that:
- learn which agents are reliable (and in what conditions)
- combine agents to improve decision accuracy
- compare against strong baselines (majority vote, averaging, weighted averaging, ideal-observer-inspired rules)

The goal is **not** to redefine the scientific question. The goal is to improve execution quality:
organization, reproducibility, efficiency, and clarity of results.

## Constraints
- Budget: **$700 total** for any paid model calls/tools.
- I have access to lab compute (GPU servers), but I still want things lightweight and reproducible.
- This should be scoped to a **5-month completion window**.
- Avoid complicated infrastructure unless it clearly helps.

## What I want from you (the VS Code agent)
Your job is to:
1) Read the current repo and identify inefficiencies (messy structure, duplicated logic, unclear scripts).
2) Improve organization and pipeline reproducibility WITHOUT changing the core objectives.
3) Propose changes as small, safe steps:
   - “Here’s the next improvement”
   - “Files impacted”
   - “Exact change + why”
   - “How we verify it didn’t break anything”
4) Prefer simple, high-leverage improvements before new modeling ideas.

## Rules of engagement
- Do NOT overwrite or “clean up” raw data.
- Do NOT rename lots of files at once.
- Do NOT introduce a complex framework (Airflow, huge refactors, etc.) unless asked.
- Always keep a runnable baseline path working.

## Definition of “making progress”
Progress means at least one of:
- a pipeline step becomes reproducible from a single command
- evaluation becomes clearer (metrics + plots + consistent splits)
- results become easier to compare across methods
- code becomes easier to extend (less duplication, clearer modules)
- experiments become traceable (configs, logs, saved outputs)

## Immediate first tasks when you start
1) Produce a short “Repo Map”:
   - main folders
   - what scripts do
   - where data is read from
   - where outputs go
2) Identify the top 3 cleanup wins (highest leverage, lowest risk).

## Tone / vibe
Keep it collaborative and straightforward. This is an undergrad thesis project, but I want it to feel like a real ML systems effort.
