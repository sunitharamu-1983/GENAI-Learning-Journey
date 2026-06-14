# Meeting Summary — JEPA: Generic Pareto-Based Reflective Prompt Optimization
**Date:** June 6, 2026
**Meeting Started:** 8:47 AM
**Duration:** 110 minutes
**Platform:** Microsoft Teams
**Instructor:** Laxmi Narayen (Applied Research Scientist, OpenStream.ai)

---

## Participants

Asha Ponraj, Devi Narayanan, Kamalam Jayaraman, Kannabiran G, Laxmi Narayen, Manoj PS, Mohamed Arsh J, Muniappan Mohanraj, Sathiyarajan Mariyappan, Sri Ranjith, Sunitha Ramu, Venkatesan Prahalanathan

---

## Session Overview

This session covered the **JEPA paper** — Generic Pareto-based Reflective Prompt Optimization — the most advanced prompt optimization algorithm in the DSPy ecosystem. The session was structured as:
1. Context setting — why JEPA exists and what problem it solves
2. Paper walkthrough — contribution statement, core claims, results
3. Deep dive into JEPA's two-stage architecture: Reflective Mutation + Pareto-based Candidate Selection
4. Code implementation in DSPy
5. Cost analysis and production considerations
6. Q&A on real-world enterprise application

---

## Part 1 — Context and Motivation (00:00 – 05:34)

### Why Prompt Optimization Matters

Laxmi opened by establishing the broader context of LLM usage:

> *"The perspective of usage of LLM for one task is now modularized — where we start to use LLMs for smaller tasks and then build up to the big holistic task itself. If that is the case, you may involve a lot of tool invocations, a lot of retrievals, and of course you may have to constrain your LLM to a lot of guardrails."*

**The problem with current approaches:**
- Reinforcement Learning (RL) based fine-tuning is expensive and computationally heavy
- Policy gradient methods (GRPO and similar) require significant resources
- Even solving small tasks like math or coding with RL requires enormous computation

**JEPA's solution:**
> *"Interpretable natural language provides much richer learning for LLMs as compared against these policy gradients or policy reward settings."*

JEPA avoids costly mathematical optimization and instead works **entirely with natural language**.

### How to Read a Research Paper (Laxmi's Method — Reinforced)

Before diving into JEPA, Laxmi reinforced her paper-reading strategy:
1. Read the **abstract** — get the problem formulation
2. Read the **last part of the introduction** — find the contribution statement
3. Jump to **methodology** — skip related works initially
4. Return to **related works** only after understanding the method

> *"The contribution statement will for sure be present in the introduction all the time."*

---

## Part 2 — JEPA Paper Walkthrough (05:34 – 20:00)

### What is JEPA?

**Full name:** JEPA — Generic Pareto-based Reflective Prompt Optimization

**Origin:** Collaborative work from **Berkeley, Stanford, Bespoke Labs, North Rhythm (France), Databricks, and MIT**

**Published at:** ICLR (International Conference on Learning Representations) — top-tier ML conference

**Video resource:** Laxmi recommended a video by **Discovery AI** that rephrases the entire paper in an understandable way. Her slides were directly based on this video.

### JEPA's Core Contribution Statement

From the paper:
> *"We introduced JEPA — Generic Pareto, a reflective prompt optimization for complex AI systems that merges textual reflection with multi-objective evolutionary search."*

**Three key claims:**
1. JEPA **mutates prompts** using natural language feedback drawn from new rollouts
2. Maintains a **Pareto front** — evolving only globally best prompts
3. **Stochastically explores** stop-performing prompts for each problem instance — enabling robust generalization and mitigating local optima

### JEPA vs Existing Approaches

| Approach | Method | Limitation |
|----------|--------|-----------|
| Greedy optimization (MiPro) | Finds best candidate, keeps improving it | Gets stuck in local optima — exploitative not explorative |
| RL-based | Scalar reward at end of rollout | Expensive, computationally heavy |
| **JEPA** | Reflective mutation + Pareto-based selection | Explorative, finds global optima, uses natural language |

**JEPA's reported results:**
> *"JEPA outperforms both MiPro and RL-based systems by a huge margin and takes significantly fewer iterations to do so."*

---

## Part 3 — JEPA Architecture: Two Stages (20:00 – 55:00)

### Overview of the Two Stages:

```
Stage 1: Reflective Evolutionary Prompt Optimizer
      ↓
Stage 2: Pareto-Based Candidate Selection
```

---

### Stage 1 — Reflective Prompt Mutation

**The student-teacher system:**

JEPA uses TWO different LLMs:

```
Small/Student Model:
→ Comes up with parent prompt (base prompt)
→ Runs it over multiple few-shot examples
→ Captures outputs, internal thoughts, tool calls
→ Passes everything to teacher model

Large/Teacher Model (e.g. GPT-5):
→ Receives full trace from student
→ Reflects on what went right/wrong
→ Gives natural language explanation
→ Proposes improved instruction candidates
```

> *"It is no more just a scalar score of the reward or the penalty that your agent performed, but rather it's going to be an explanation of what went right or what went wrong as well."*

**What makes this "reflective":**
- The teacher model diagnoses problems in natural language
- Proposes specific prompt updates
- Tests those updates
- This cycle repeats — each iteration the prompt gets better

**The meta-prompt:**
The smaller model generates what Laxmi called an **"intermediate instruction template"** — a meta-prompt given to the teacher LLM that specifies:
1. What to look for in the student's output
2. What the goal is
3. What should be fixed

> *"This is the optimizer itself. And then finally we are going to get the meta-prompt — the intermediate instruction template that we will have to give to the meta-optimizer telling the senior LLM what to look for and what is the goal."*

**What "prompt failure" means:**
Devi Narayanan asked a key question: *"When will we say a prompt has completely failed?"*

Laxmi's answer:
> *"We will say it has failed when the outputs are not proper based on the score only. Everything will give an answer. That answer is not good — that's what they mean by prompt failure."*

**The mutation mechanism:**
1. Start with ONE base instruction
2. Generate 3-4 different detailed instruction candidates from it
3. Evaluate each candidate
4. Keep the best ones
5. Mutate the best ones further
6. Repeat

> *"We are not going to do an exhaustive exploitative search — one that moves from zero to one to two to three. No. We are going to have multiple branches of candidates and then finally select the best mutated candidate."*

---

### Stage 2 — Pareto-Based Candidate Selection

**The explore vs exploit dilemma:**

Every optimizer faces this:
- **Exploit:** Find something that works and keep making IT better
- **Explore:** Try multiple different solutions

**MiPro's failure point:**
MiPro V2 uses bootstrapping — it selects the best combination of candidates that work well together. Laxmi argued this is fundamentally exploitative — it doesn't explore diverse enough solutions.

**JEPA's solution — the Pareto Front:**

> *"The core idea is not about finding a single champion, but rather pushing forward a frontier of diverse non-inferior specialists. The best solution could come from anybody — that's the possibility we are trying to explore."*

**The manager analogy:**

Laxmi used a brilliant hiring analogy:

```
Greedy Manager:
→ Hires the world-record PhD in control systems
→ Builds entire team around ONE person
→ Short-term optimal — but misses edge cases
   that even this expert can't handle!

JEPA Manager:
→ Assembles an ENSEMBLE of smaller experts
→ Math specialist, writing specialist, balanced generalist
→ Best breakthrough could come from ANY of them!
→ That's Pareto search!
```

**How Pareto selection works:**

The algorithm iterates over every prompt and asks:
> *"Is there any other prompt in the pool that scores higher than this one on at least one task without scoring lower on the other?"*

- If **YES** → prompt is **dominated** → temporarily ignored
- If **NO** → prompt is **non-dominated** → added to elite Pareto front pool

**Concrete example (Math vs Writing tasks):**

```
P_math: Excellent at math, poor at writing
P_writing: Excellent at writing, poor at math
P_balanced: Midway on both tasks
P_dominated: Another prompt beats it on BOTH tasks

Pareto front keeps:
→ P_math ✅ (best at math, even if dominated on writing)
→ P_writing ✅ (best at writing)
→ P_balanced ✅ (not dominated on either)
→ P_dominated ❌ (discarded)
```

**Stochastic selection for next mutation:**

From the Pareto front, JEPA decides who gets mutated next using **weighted lottery** (stochastic selection):

```
Better performing candidates:
→ Higher weightage in lottery
→ Get mutated MORE times

Lower performing candidates:
→ Lower weightage
→ Still in lottery — not ignored completely!
→ Prevents premature convergence
```

> *"The ones that score better will have more chance to be mutated. And the one that scores less will have lesser chance of being randomly selected for the next mutation, but rather will still be given a chance — it will not be neglected completely."*

---

### Stochastic Selection — AdaBoost Analogy

Mohamed Arsh J asked about the stochastic selection mechanism. Laxmi connected it to **ensemble learning in machine learning:**

**AdaBoost parallel:**

```
Model 1 trained on full dataset:
→ 100% on Sample 1 ✅
→ 100% on Sample 3 ✅
→ 50% on Sample 4 ⚠️
→ 25% on Sample 5 ❌
→ 1% on Sample 6 ❌

Bootstrap Dataset for Model 2:
→ Sample 4 represented 2x ← misclassified
→ Sample 5 represented Nx ← misclassified
→ Sample 6 represented Nx ← misclassified

Model 2 focuses on Model 1's mistakes!
      ↓
Combination of Model 1 + Model 2 = stronger! ✅
```

> *"This is explorative — not just making one model better on all rows, but rather having Model 2 learn from mistakes of Model 1, then Model 3 and so on and so forth."*

**Sunitha Ramu asked for an example of stochastic selection** — Laxmi used exactly this AdaBoost analogy and confirmed Sunitha's understanding.

**Key insight from Mohamed Arsh J:**
> *"Adding noise to generalize it."*

Laxmi confirmed: exactly — the stochastic weightage adds controlled noise to prevent the optimizer from getting stuck.

> *"The best from the elite pool are given more and more weightages so they get more picked in the lottery tickets for better mutation. The ones that are low will still be present in the lottery but rather won't be selected much. So this is a balance that JEPA maintains between exploration and exploitation — that MiPro failed to achieve."*

---

## Part 4 — The JEPA Paradox (01:00:00 – 01:02:00)

Mohamed Arsh J raised a key issue: **the role of the meta-optimizer**

Laxmi articulated the **JEPA Paradox:**

> *"The whole performance of this algorithm banks on the powerfulness of the meta-optimizer itself."*

**The problem:**
- The more you use the teacher model (large cloud LLM), the more expensive it gets
- The teacher model must understand the entire chain of thought, logs, function calls — at a humongous level
- Without proper causal reasoning, generating new instructions won't be proper

> *"It can't just fix smaller bugs, but rather it has to get through the whole concept of understanding, reasoning, logs, and the input at a humongous level to even make a small change."*

**The paradox:**
> *"How can we easily optimize or have a weaker model for meta-optimizer? This is an open research direction. A really good prompt optimizer system — but how can we optimize that meta-optimizer? Food for thought."*

This is explicitly called **"the JEPA paradox"** in the session.

---

## Part 5 — DSPy Implementation of JEPA (01:36:00 – 01:45:00)

### Setup

```python
import dspy
from dspy.teleprompt import JEPA

# Initialize reflection model (teacher — needs to be powerful!)
reflection_lm = dspy.LM(
    model="openai/gpt-4o",  # or GPT-5 as Laxmi used
    api_key="your_key_here"  # mask before sharing!
)

# Initialize student model (smaller, local)
student_lm = dspy.LM(
    model="ollama_chat/qwen2.5",
    api_base="http://localhost:11434"
)

dspy.configure(lm=student_lm)
```

### Evaluation Metric

```python
def intent_match_metric(example, prediction, trace=None):
    """
    JEPA returns: original, prediction, score
    We check if predicted intent matches ground truth
    """
    return example.answer.lower() == prediction.answer.lower()
```

### Initializing and Running JEPA

```python
# Initialize JEPA optimizer
jepa_optimizer = dspy.JEPA(
    metric=intent_match_metric,      # evaluation function
    reflection_model=reflection_lm,  # teacher LLM
    num_threads=10,                  # parallel processing
    auto="light"                     # light/medium/heavy
)

# Compile (runs the full optimization loop)
compiled_jepa = jepa_optimizer.compile(
    student=cot_predictor,
    trainset=train_examples,
    valset=dev_examples
)
```

### The `auto` Parameter — Three Levels:

| Level | Cost | Speed | Use Case |
|-------|------|-------|----------|
| `light` | ~$0.13–$0.46 | Fast | Rapid prototyping, quick feedback |
| `medium` | ~$2–$2.50 | Medium | Balanced cost vs quality |
| `heavy` | $10+ | Slow | Production workloads, in-depth search |

> *"Light is usually for rapid prototyping and feedback. Medium is for balance between API cost and compute time. Heavier models are for production workloads where you do an in-depth search."*

### Results from Laxmi's Run:

**Setup:**
- Model: GPT-5 (teacher) + Olama (student)
- Optimization steps: 560
- Mode: `auto="light"`
- Total cost: **$0.13 today + $0.26 from yesterday = ~$0.46 total**

**Scores achieved:**
- Validation set: **75%**
- Test set: **~73%**

**Comparison:**
```
Light mode (JEPA):   73-75%
Medium mode:         ~80%+ (estimated)
Heavy mode:          Higher (estimated)
```

> *"On medium I may get more than 80 and on heavy I'll get more, but the catch is that I'm not using just Olama anymore. I'm also involving another reflection model that's quite heavy on my shoulders."*

### Example of JEPA-Generated Prompt (Iteration 1 → 13):

**Starting prompt (iteration 1):**
```
Propose a new text for predict. We are given customer message and intent label. 
The task is output exactly one predicted class intent. The output must be one 
label chosen from the intent. Do not output multiple labels. How to choose 
the label? Match the user's main intent and then use these domain mapping 
synonyms, actis, air style travel domain...
```

**After 13 iterations:**
A significantly more refined prompt emerged that scored 75% on validation. The full evolution was shared via WhatsApp and GitHub.

---

## Part 6 — Cost Analysis and Enterprise Use (01:04:00 – 01:20:00)

### DSPY in Development vs Production

A critical clarification from Kannabiran G's question:

> *"DSPY will never be used in a real-time system. DSPY is designed to be a system that you work with during development — it's a compile-time system. You work with generating a prompt and optimize the prompt during development time. This prompt can run more efficiently during production time."*

```
Development (DSPy):
Run JEPA optimization → JSON saved
~$0.46–$2.50 one-time cost

Production:
Load JSON → hit LLM with optimized prompt
Per query: fraction of a cent ✅
No re-optimization needed! ✅
```

### Cost Reality Check

Laxmi shared her actual OpenAI usage costs:
- 560 optimization steps with GPT-5 teacher model
- Total spend: **~$0.46** (light mode)
- Medium mode: **~$2–$2.50**
- Heavy mode: **$10+**

> *"It is costly, but it is not as costly as you would expect an organization to call it costly. It's roughly $1-2 and this is a one-time optimization step. I'm sure the company can spend one or two dollars for one-time optimization and later use this prompt for production."*

### Using Cloud LLMs Instead of Olama

Kannabiran asked about enterprise restrictions on local LLMs. Laxmi's answer:

> *"I have been using DSPy with Olama for class because not all of them will have access to cloud LLMs. But this same DSPy can also be used with cloud LLMs — OpenAI, Gemini, or whatever your company affirms to."*

**Enterprise approach:**
1. Get temporary API keys for POC (2 weeks typically)
2. Run DSPy optimization once → save JSON
3. Present results to leadership
4. If approved → get permanent API access for production
5. Cost reviews happen monthly in enterprise settings

---

## Part 7 — Context Management in Production (01:12:00 – 01:16:00)

Kannabiran G raised an important production concern: when users have long conversations, the entire history gets passed to the LLM — consuming massive tokens.

Laxmi distinguished between two different problems:

```
Problem 1: History of OPTIMIZATION RUNS (DSPy)
→ What DSPy needs to generate better prompts
→ Managed by DSPy internally

Problem 2: History of CHAT SESSIONS (production)
→ Long conversations consuming token budgets
→ Needs separate handling
```

**Four strategies for managing context in production:**

1. **Context Compression / Hierarchical Summary:**
   > *"We pass a summary of whatever is happening — a hierarchical summary. So that way you don't have to pass the exact words that you spoke to an LLM, but rather just pass a small chunk of it."*

2. **Observation Masking / Sliding Window:**
   > *"We do a sliding window of just the recent messages, dropping the old ones entirely."*

3. **Prompt Caching:**
   Cache generated prompts so they don't need to be regenerated every time. Reduces cost by 50%+.

4. **Attitude Tuning:**
   Guide the model's behavior without hardcoding a huge list of edge cases in guardrails. As the prompt grows very big, this becomes important.

---

## Part 8 — SQL Query Chains for Enterprise Data (01:17:00 – 01:19:00)

Kannabiran G described his enterprise challenge: billions of records across thousands of tables in multiple layers (Hive, Oracle, business rule systems).

Laxmi's recommendation:

> *"Look at the SQL query chains. In LangChain and LangGraph, you have something called as SQL query chain. It's absolutely suited for large databases like yours. I have implemented one for a freelancing project I was working on."*

**Why SQL query chain works:**
> *"It won't go to the whole rows of the table, but rather it will start generating SQL queries, so hallucinations will also reduce about the data."*

**Note from Laxmi:** This is also available in open source and works well for smaller tables. Enterprise scale (thousands of tables) may need additional architecture discussion.

---

## Part 9 — Q&A Highlights

### Devi Narayanan — Prompt Failure Definition
**Q:** When will we say a prompt has completely failed?
**A:** When the score it produces is not good — not when it fails to give an answer (LLMs always give an answer), but when that answer is wrong based on the evaluation metric.

### Mohamed Arsh J — Role of Particular Model
**Q:** What role does the particular model take while answering?
**A:** Excellent point — if you use the teacher model more and more, you will be charged more. The whole performance banks on the powerfulness of the meta-optimizer. This is the JEPA paradox.

### Sunitha Ramu — Stochastic Selection Example
**Q:** Can you give an example for stochastic selection?
**A:** Laxmi gave the AdaBoost/ensemble learning example. Sunitha confirmed understanding and connected it to JEPA's weighted mutation lottery.

### Kannabiran G — DSPY in Production
**Q:** Can DSPy be used in real-time production?
**A:** No — DSPy is a development/compile-time tool. The OUTPUT (JSON) is used in production, not DSPy itself.

### Kannabiran G — Context Window Cost
**Q:** How to handle growing context in long user sessions?
**A:** Four strategies: hierarchical summary, observation masking/sliding window, prompt caching, and attitude tuning.

---

## JEPA vs MiPro V2 — Final Comparison

| Feature | MiPro V2 | JEPA |
|---------|----------|------|
| Optimization type | Bayesian + Bootstrap | Reflective mutation + Pareto |
| Search strategy | Exploitative (greedy) | Explorative (Pareto front) |
| Feedback type | Scalar score | Natural language explanation |
| Number of LLMs | One | Two (student + teacher) |
| Local optima risk | Higher | Lower (Pareto prevents it) |
| Cost | Lower | Higher (teacher model needed) |
| Score (ATIS, light) | ~68-69% | ~73-75% |
| Score (OpenAI) | ~88-95% | Higher (estimated) |
| Complexity | Medium | High |
| Production use | JSON | JSON |

---

## Key Concepts — Quick Reference

| Concept | Definition |
|---------|-----------|
| JEPA | Generic Pareto-based Reflective Prompt Optimization — most advanced DSPy optimizer |
| Reflective Mutation | Student LLM generates prompt → teacher LLM reflects and improves it in natural language |
| Pareto Front | Set of non-dominated candidates — diverse specialists, not just one champion |
| Dominated Prompt | Another prompt beats it on ALL tasks → discarded |
| Non-Dominated Prompt | No other prompt beats it on ALL tasks → kept in Pareto front |
| Stochastic Selection | Weighted lottery — better candidates mutated more, worse ones still given a chance |
| Greedy Search | Exploitative — keeps improving ONE best candidate |
| Pareto Search | Explorative — maintains diverse frontier of specialists |
| JEPA Paradox | The meta-optimizer needs to be very powerful — but how do you optimize the meta-optimizer? |
| auto="light" | ~$0.46, fast, good for prototyping |
| auto="medium" | ~$2.50, balanced |
| auto="heavy" | $10+, production grade |
| Context Compression | Passing hierarchical summary instead of full conversation history |
| Observation Masking | Sliding window — only recent messages sent to LLM |
| SQL Query Chain | LangChain tool for querying large databases via generated SQL — reduces hallucination |
| AdaBoost analogy | Misclassified samples get higher representation in next learner — same as JEPA's stochastic weightage |

---

## Resources Shared

| Resource | Details |
|----------|---------|
| Discovery AI video | Video that rephrases the JEPA paper in understandable terms — Laxmi's slides based on this |
| JEPA paper | Published at ICLR — from Berkeley, Stanford, Bespoke Labs, North Rhythm, Databricks, MIT |
| JEPA notebook | Shared via WhatsApp (Teams connection issues prevented sharing in chat) |
| Gen AI GitHub repository | Participants asked to push JEPA notebooks to the shared repository |

---

## Next Session

Laxmi indicated the next session would cover:
- **RAG (Retrieval Augmented Generation)**
- **Vector databases**
- **LangChain and LangGraph**

> *"Just take a look at it and come back tomorrow. Let's discuss on vector basis and so on."*

---

## Technical Issues

Microsoft Teams chat file sharing failed during this session — Laxmi attempted to share the JEPA notebook via Teams chat but the files did not appear. She eventually shared via **WhatsApp** instead and mentioned she would push to GitHub.

---

*Summary prepared from meeting transcript dated June 6, 2026.*
