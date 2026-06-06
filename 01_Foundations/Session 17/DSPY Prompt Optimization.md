# Meeting Summary — Bootstrap Few Shot Random Search, MiPro V2 & Bayesian Optimization
**Date:** May 24, 2026
**Meeting Started:** 8:35 AM
**Duration:** 97 minutes
**Platform:** Microsoft Teams
**Instructor:** Laxmi Narayen (Applied Research Scientist, OpenStream.ai)

---

## Participants

Akash Balmiki, Asha Ponraj, Bineetha Gooinathan, Devi Narayanan, Kamalam Jayaraman, Kannabiran G, Laxmi Narayen, Manoj PS, neelsvel1, Parthasarathi, Pon Ezhil, Sathiyarajan Mariyappan, Shobana Samyayyah, Sunitha Ramu

---

## Session Overview

This session was a direct continuation of the May 23 session. It covered:
1. Recap Q&A on saving/loading optimized prompts and DSPy enterprise use
2. DSPy relationship to Meta Prompting — clarification
3. Bootstrap Few Shot Random Search — the next optimizer beyond basic bootstrap
4. Evaluation results — comparing all optimizers
5. MiPro V2 — the paper walkthrough and algorithm deep dive
6. Bayesian Optimization and Optuna library
7. MiPro V2 code implementation
8. Assignment — Read the JEPA paper

---

## Part 1 — Recap Q&A (00:00 – 05:30)

### Saving and Reusing Optimized Prompts

**Kannabiran G's question:** Once optimization is done, do we need to re-optimize every time?

**Laxmi's answer:**
> *"Once the optimization is done, you can just go on to save using dot save. If you open it, you will get to see the few shot examples plus the actual prompt itself present in the JSON. The prompt is optimized and saved — you can use it for further processing."*

**Workflow:**
```
Run optimization (once) → Save as JSON → Load JSON → Use for predictions
→ No need to re-optimize unless there are new failure cases!
```

### Synthetic Query Generation

**Kannabiran G confirmed:** DSPy auto-generates synthetic queries not present in the dataset (approximately 10) and evaluates them alongside the few shot examples.

### Enterprise Use of DSPy

**Kannabiran G's question:** DSPy is open source — can it be used for enterprise purposes?

**Laxmi's answer:**
> *"Yes, definitely. This is an open source framework. But it depends on the regulations of your organization. If you don't want it to see all the data, maybe you can synthesize data similar to your data as well, mask important information, and then use it as well."*

---

## Part 2 — DSPy and Meta Prompting Relationship (01:32 – 03:27)

### Devi Narayanan's Question:

> *"Is DSPy part of meta prompting or is it done after meta prompting to optimize the prompts generated?"*

### Laxmi's Answer — Layered Explanation:

**Level 1 — DSPy IS meta prompting:**
> *"Under the hood, this is a meta-prompting framework. Meta prompting is the use of LLM to write or critique a prompt. DSPy uses the exact concept to turn it into an automated prompt."*

**Level 2 — DSPy goes BEYOND meta prompting:**
> *"DSPy automates meta prompting itself. Meaning, in manual meta prompting, you have to go enter your task into an LLM, the LLM reads the task and starts giving you a prompt. Here, DSPy automates even that step — it's one step OVER meta prompting."*

**Sunitha Ramu's sharp clarification:**
> *"If it is generating only prompts, it is meta prompting. But here, it not only generates the prompts — it also generates results!"*

**Laxmi confirmed:**
> *"Exactly. It also generates the result using the prompt it has already generated. So it's like automating meta prompting itself — one step over meta prompting itself."*

### Summary:

| Technique | What it does |
|-----------|-------------|
| Meta Prompting (manual) | You ask LLM to write a prompt → LLM gives you a prompt → You use it |
| DSPy | Automatically writes the prompt AND uses it to generate the result — full automation |

---

## Part 3 — Important Terminology Clarification

**Kannabiran used the word "predict" for DSPy optimization.**

**Laxmi corrected:**
> *"Optimize the prompt is the word. Don't use the word predict. Prediction would mean within a given set of words it has to select words — natural language doesn't have that luxury. It's optimizing the prompt."*

**Correct mental model (Kannabiran confirmed):**
> *"Whenever we are provided with a task, we need to optimize and store it as a JSON file. It will help to get the accurate result."*

---

## Part 4 — Bootstrap Few Shot Random Search (05:32 – 25:00)

### What is Bootstrap Few Shot Random Search?

This is a more powerful optimizer than basic Bootstrap Few Shot. It introduces **hyperparameter optimization** via random search.

**Laxmi's Athletic Analogy:**

> *"Think of Bootstrap Few Shot optimization as 400 meters or 100 meters — where just one runner runs. This few shot random search is like a relay — but don't think of relay as sequential run. Think of relay as a team running AGAINST another team."*

```
Bootstrap Few Shot:         Bootstrap Few Shot Random Search:
One runner (one path)       A relay team (multiple parallel paths)
↓                           ↓
Single optimization         Multiple combinations searched in parallel
```

### How It Works — The Drawing Explained:

Laxmi drew on the Microsoft Teams whiteboard to explain:

```
SYNTHETIC EXAMPLES:         REAL EXAMPLES:
Synthetic Ex 1              Real Ex 1
Synthetic Ex 2              Real Ex 2
Synthetic Ex 3              Real Ex 3
Synthetic Ex 4              Real Ex 4
Synthetic Ex 5              Real Ex 5

COMBINATIONS TRIED:
S1 + R2 → evaluate
S2 + R1 → evaluate
S1 + R3 → evaluate
S3 + R2 → evaluate
... all combinations explored
↓
Best combination selected! ✅
```

> *"It does not settle for just one batch of successful synthetic candidates. Rather, it creates multiple combinations of examples, multiple variations of real life examples, and multiple variations of synthetic combinations — and sees what is the best group."*

### Key Parameters:

```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch

bootstrap_random = BootstrapFewShotWithRandomSearch(
    metric=dspy.evaluate.answer_exact_match,  # grading rule
    max_bootstrapped_demos=10,                # hard ceiling for generated examples per candidate
    num_threads=4,                            # parallel processing workers
    num_candidate_programs=5                  # 5 completely different versions to try
)
```

**Parameter explanations:**

| Parameter | Meaning |
|-----------|---------|
| `max_bootstrapped_demos` | Hard ceiling — max generated examples in any single prompt candidate |
| `num_threads` | Activates parallel processing — searches multiple combinations simultaneously |
| `num_candidate_programs` | Creates N completely separate versions of the pipeline with unique randomized mixes |

> *"Number of threads activates parallel processing because it has to search — go through combinations, mix and match multiple combinations of the best ones."*

> *"Number of candidate programs is equal to 5. This is the heart of the random search process. DSPy will compile and generate 5 completely separate versions of our pipeline. Each candidate program will contain a unique randomized mix of different bootstrapped and different label candidates."*

### Runtime and Results:

> *"3 minutes for one optimization. For me, I think it runs for more than half an hour or so. So I'll let you guys run this in your own pace."*

**Result of random search run:**
- 10 total examples selected
- 1 synthetic example + 9 real examples
- Validation performed on dev examples
- Best score achieved: **69.44%** on validation set

### Saving and Loading — Demo:

```python
# Save optimized prompt
compiled_random.save("cot_bootstrap_fewshot_random.json")

# Load for future use (no re-optimization needed!)
loaded_program = dspy.ChainOfThought(IntentClassification)
loaded_program.load("cot_bootstrap_fewshot_random.json")
```

---

## Part 5 — Production Considerations (14:00 – 25:00)

### How Much Training Data for Production?

**Sathiyarajan's question:** For the random search, it tries N times. If we have 100 records, would it check all 100 scenarios — causing latency?

**Laxmi's answer:**
> *"Exactly. That's why we feed a subset of the whole training data. We only feed 2 examples per intent. You can try with 10 examples per intent, but feeding the whole training data would run for a really long time."*

**Laxmi's production experience:**
> *"In our use case, we just used roughly 30 to 40 examples — not more than that. We had optimized once, and once optimization is done, we saved it and loaded it and just sent it to production."*

**Practical limit:**
> *"These prompt optimization techniques aren't programmed to work with millions and millions of rows. These can work with just a smaller subset only. 100 to 500 rows is the practical maximum."*

### What if Dataset Has Millions of Rows?

**Asha's question:** In real production with a large dataset, what do you do?

**Laxmi's recommended approach:**
1. Take a **representative subsample** (100-500 rows)
2. Run optimization on the subsample
3. Test on a bigger subset — does it work?
4. If it fails on some cases → include those failure cases in the subsample
5. Re-optimize with failure cases added
6. **Iterative procedure** — repeat until quality is acceptable

> *"It's not that you cannot run million rows — you can — but it's going to take so much time. I've tried and it's not quite fit for that."*

### Cost Reduction Strategies for Commercial APIs:

**Kannabiran G's question:** In enterprise with paid LLM APIs, how many API calls does DSPy make? Is it cost-effective?

**Laxmi's answer:**

Estimated API calls for 100 training rows × 50 validation examples:
> *"Roughly 100 × 50 = 5,000 max total API calls — it'll make like 1,500 to 3,000 realistically."*

**Three cost reduction strategies:**
1. **Prompt Caching** — Cache generated prompts. Don't rerun everything. Just revisit cached prompts → **reduces cost by at least 50%**
2. **Batch APIs** — Use batch API calls instead of running one by one
3. **Teacher-Student Learning** — Have a small, cheap local LLM taught by the expensive API LLM (teacher-student paradigm)

### When to Update the JSON / Re-optimize?

**Asha's question:** How frequently should the JSON be updated?

**Laxmi's thumb rule:**
> *"I don't touch something when it runs. I build it once. When everything is going fine, that's when you should NOT touch it."*

**When to re-optimize:**
- When the client reports a specific failure case
- When you've backtracked and identified which step in the pipeline failed
- When you find a new failure case scenario → add to training set → re-optimize

> *"Only when intervention is needed will you have to intervene."*

### Production Architecture (Shobana's clarification):

> *"DSPY will be executed during development time. Have the JSON saved. In your application, your API (FastAPI) will use that JSON to hit the model for predictions."*

**Laxmi confirmed:**
> *"Yes, or you can also use DSPY to finally load it. You don't have to optimize again — just load it and get the predictions."*

```
Development:
DSPY optimization → JSON saved

Production:
FastAPI loads JSON → sends to LLM → gets predictions
(No DSPY optimization loop in production!)
```

---

## Part 6 — Evaluation Results — All Optimizers Compared (28:00 – 32:00)

### Score Comparison Table:

| Optimizer | Score on Test Set |
|-----------|------------------|
| Chain of Thought (Zero Shot) | **40%** |
| Few Shot + Chain of Thought | **46.7%** |
| Bootstrap Few Shot | **~47–57%** |
| Bootstrap Few Shot Random Search | **57.88%** |
| MiPro V2 (Olama) | **~68–69%** |
| MiPro V2 (OpenAI GPT) | **~88–95%** |

**Notes:**
- All Olama results used a quantized model — not very powerful, but effective
- OpenAI models gave dramatically better scores (88-95%) on the same task
- **F1 score is recommended for production** (not exact match) — especially for imbalanced datasets

### Why F1 Score in Production?

**Sunitha Ramu asked:** Why are we not using F1 score?

**Laxmi's answer:**
> *"You can use anything. But for real-time production use only F1 score, because we would want to make sure all intents are balanced and classified. Exact match here was just to see if it even matches at a basic level. If this scored 90-100%, THEN it would make sense to look at intent-wise F1."*

### Does the Same JSON Work Across Different Models?

**Sunitha's question:** If I save a JSON from Olama and then run it with OpenAI, will I get the same score?

**Laxmi's answer:**
> *"The JSON format should work across models (it's based on the signature). But you may not get the same score — model parameters are different, model understanding differs. You may need to rerun the JSON optimization for the new model."*

**Shobana confirmed:** The format (prompt structure, signature) should be compatible — but model-specific performance will vary.

---

## Part 7 — MiPro V2 Paper Walkthrough (32:00 – 57:00)

### How to Read a Research Paper (Laxmi's Method):

> *"I read a paper like this: I read the abstract. I read the last part of the introduction (where the contribution statement is). Then I go to the methodology. This way I bypass the noise of related works. I come back to related works only after I finish the methodology."*

**Why this approach:**
> *"Contribution statement will be very easily present in the final part of the abstract AND the last part of the introduction. This way you understand their method vs how they compare against other papers."*

### Paper: MiPro V2

**Full title:** *"Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs"*

**Full algorithm name:** **Multi-Prompt Instruction Proposal Optimizer (MiPro V2)**

### What Problem MiPro Solves:

> *"Language model programs are increasingly sophisticated pipelines of modular language calls. Building these pipelines requires creating prompts that are jointly effective for ALL modules."*

> *"Current language model programs aren't made of single language model calls — they're made of multiple modular language model calls. These need prompts optimized for ALL these modules."*

### Three Contributions of MiPro V2:

**Contribution 1 — Formalization:**
Formalizes the problem of optimizing language model programs. Proposes an algorithm design space with 3 strategies to address the challenge of **prompt proposal**.

**Contribution 2 — Three strategies for prompt proposal:**
1. **Bootstrap Task Demonstrations** — find good few shot examples
2. **Propose Candidate Instructions** — write contextually aware instructions
3. **Bayesian Optimization** — find the best combination

**Plus:** Three strategies to resolve **credit assignment** — assigning a score/credit to each proposed prompt.

**Contribution 3 — Benchmark:**
Constructs and evaluates a rich subset of possible algorithms for prompt optimization across 7 tasks.

### MiPro V2 Result:
> *"Outperforms baseline optimizers on 5 of 7 tasks in a benchmark by as much as 13% accuracy improvement."*

### Michael J. Ryan — Stanford:
Laxmi referenced an interview with Michael J. Ryan (master's student at Stanford who co-authored DSPy/MiPro work):
> *"He said they started with 7 tasks and are open to expanding to 30 different tasks."*

---

## Part 8 — MiPro V2 Algorithm — Three Stages Deep Dive (47:00 – 57:00)

### Stage 1 — Bootstrap Task Demonstrations

*This is the same as what we already know from Bootstrap Few Shot.*

```
Training data + Language model + Metric
↓
Find bootstrap few shot examples from training set
↓
Evaluate: are the answers good?
→ YES: retain the few shot examples ✅
→ NO: redo finding examples ❌
↓
Best few shot demonstrations selected
```

### Stage 2 — Propose Candidate Instructions

This is NEW compared to what we saw before. MiPro doesn't just find few shot examples — it also **writes the instructions** themselves.

**What instructions need to contain:**
- Program awareness (understands where this module sits in the whole program)
- Data awareness (understands what data is being used)
- Demo awareness (understands the few shot examples)
- Example awareness
- **Prompting tips** (e.g., "don't be afraid to be creative", "you are working in a high-stake environment")

**The process:**
```
Program code + Data + Few shot examples + Prompting tips
↓
ALL fed into the LLM (Olama/OpenAI)
↓
LLM generates MULTIPLE candidate instructions:
→ Candidate 1: "Given a context and a question, generate a detailed accurate answer..."
→ Candidate 2: "Given context about a topic, generate a precise answer..."
→ Candidate 3: ...
→ Candidate 4: ...
↓
Multiple instruction candidates produced
```

**Sunitha Ramu's insight (confirmed by Laxmi):**
> *"This is based on the signature — it already wrote instructions from the signature. When using MiPro, we have multiple combinations of the system."*

**Laxmi confirmed:**
> *"MiPro will have multiple combinations of these instructions and the few shot examples. It will optimize and see which combinations work well. Based on your metric (F1 score), whichever combination gives the maximum F1 score — that will be taken as the best model."*

### Stage 3 — Bayesian Optimization (via Optuna)

**What is Bayesian Optimization?**

> *"A mathematically grounded optimization. Given multiple instruction sets, multiple demo sets, multiple combinations of subsets — it tries to see what is the optimal combination such that my score becomes higher."*

**The mathematical basis — Bayes Theorem:**
> *"It's trying to find the probability of variable A given variable B. MLE — Maximum Likelihood Estimation — tries to find how to maximize the probability of such a classification given these scenarios."*

```
Multiple instruction candidates (from Stage 2)
+ Multiple demo combinations (from Stage 1)
↓
Bayesian optimization tries all combinations
↓
"Which combination of instructions + demos makes the best pair?"
↓
Evaluates on FULL train set across N trials
↓
Best combination selected ✅
```

**Why we need Bayesian optimization vs random search:**

| Random Search | Bayesian Optimization |
|--------------|----------------------|
| Tries combinations randomly | Tries combinations probabilistically |
| No learning between trials | Learns from previous trials |
| May miss best combination | More efficiently finds optimal combination |
| Fixed budget of trials | Focuses trials on promising regions |

### Optuna Library:

> *"There is this library called Optuna. What it does is basically it creates Bayesian optimization and Bayesian hyperparameter tuning via the particular metrics. Very effective — all you have to do is give your model and the data. It will run what should be the best likelihood given these metric type optimizations multiple times, and give you the best score automatically."*

> *"The DSPY library also uses Optuna in the background."*

---

## Part 9 — MiPro V2 Code Implementation (1:25:00 – 1:34:00)

### The Three Steps MiPro Runs Automatically:

```
Step 1: Bootstrap few shot example finding
↓
Step 2: Propose candidate instructions
↓
Step 3: Bayesian optimization (finds best instruction + demo combination)
↓
Best optimized prompt! ✅
```

### Code:

```python
from dspy.teleprompt import MIPROv2

# Define MiPro V2 optimizer
mipro_optimizer = MIPROv2(
    metric=dspy.evaluate.answer_exact_match,  # evaluation metric
    num_threads=4,                             # parallel workers
    auto="light"                               # lightweight trial budget
)

# Compile (this is the master compilation loop)
compiled_mipro = mipro_optimizer.compile(
    student=cot_predictor,           # model to optimize
    trainset=train_examples,         # training examples
    valset=dev_examples,             # validation examples
    requires_permission_to_run=False # flag: yes I know this will make many API calls
)
```

### Parameter: `auto="light"`

> *"When we say auto equals light, it applies a very low weight trial budget — meaning it will limit the number of trials to 10,000-20,000. So this is a lightweight handle over such computationally heavy Wipro stuff."*

**Why `requires_permission_to_run=False`:**
> *"MiPro runs a heavy optimization loop. It has to make a large number of calls to any API model. This flag is saying: I know what I'm doing — this is going to make a lot of calls but I'm fine with it."*

### MiPro V2 Results:

**On validation set:**
- Best score achieved: **68.89%**

**On test set:**
- Best result across all optimizers: **~69%**

**Prompt output structure:**
```
Augmented true message (the query)
+ Examples (few shot demonstrations)  
+ Instructions (candidate instruction written by LLM)
+ Fields (signature fields)
= Final optimized prompt ✅
```

---

## Part 10 — Generation Comparison — All Optimizers (25:00 – 27:30)

Laxmi contextualised all optimizers as belonging to two generations of prompt optimization:

### First Generation Prompt Optimization:
- Chain of Thought (Zero Shot)
- Bootstrap Few Shot
- Bootstrap Few Shot with Random Search

> *"These are the smaller optimizers as compared against current generation ones — the current research ones do these optimizations on steroids."*

### Second Generation / Hybrid Prompt Optimization:
- MiPro V2 (combines all three strategies)

> *"Just like how we had first generation prompting — manual prompts. Then second generation mixes and matches multiple prompts fluently in hybrid. Same with prompt optimization. First generation: chain of thought or bootstrap or bootstrap with random search. Next generation: hybrids of these methods."*

> *"That's how research plays, right? You read a research paper. You see how to mix A with B, use it for a different task C. That's another paper — applied research."*

---

## Part 11 — Benchmark Comparison (1:26:35 – 1:28:00)

Laxmi showed the benchmark results from the MiPro V2 paper:

```
Zero Shot approach:           Decent baseline
Bootstrap approach:           Jumps significantly from zero shot ↑
MiPro V2 approach:            Best score — achieved via Bayesian optimization ↑↑
```

> *"The MiPro approach goes on to find the best score, and this best score is achieved via Bayesian optimization."*

---

## Part 12 — Assignment (1:34:56 – 1:36:40)

### Assignment: Read the JEPA Paper

**What:** Read the **JEPA paper** (Generic Pareto-Based Prompt Optimization)

**Conference:** ICLR — International Conference on Learning Representations
> *"This is from a very important conference called ICLR — a very top tier conference."*

**Task:**
1. Read the paper
2. Take notes
3. Create a report / summary
4. Come back and present

> *"This is to inculcate the habit of reading papers. Look at this, take notes, read it, create a report, and come back. We will see this and how to use this as an optimizer."*

**Deadline:** Next to next Saturday (note: next week is a holiday due to Bakrid long weekend)

### Holiday Notice:
> *"Next week will be a holiday for all of you because of Bakrid long weekend. Please note."*

---

## Resources Shared at End of Session:

1. **DSPY Training notebook** (Olama version)
2. **DSPY Training notebook** (OpenAI API version)
3. **JSON files** — pre-optimized prompt JSONs from each optimizer (for comparison)
4. **MiPro V2 PPT** — Ryan's presentation from Stanford
5. **JEPA paper** — shared for assignment

---

## Key Concepts — Quick Reference

| Concept | Definition |
|---------|-----------|
| Bootstrap Few Shot Random Search | Multi-combination search: tries N synthetic + N real example combinations in parallel to find the best group |
| Num Threads | Activates parallel processing — searches multiple combinations simultaneously |
| Num Candidate Programs | Number of completely separate pipeline versions created — each with unique randomized mix |
| MiPro V2 | Multi-Prompt Instruction Proposal Optimizer Version 2 — hybrid algorithm combining Bootstrap + Instruction Proposal + Bayesian Optimization |
| Stage 1 (MiPro) | Bootstrap Task Demonstrations — finds best few shot examples |
| Stage 2 (MiPro) | Propose Candidate Instructions — LLM writes multiple instruction candidates |
| Stage 3 (MiPro) | Bayesian Optimization — finds best combination of instructions + demos |
| Bayesian Optimization | Probabilistic optimization that learns from previous trials to efficiently find optimal combinations |
| MLE | Maximum Likelihood Estimation — mathematical basis for finding best probability of correct classification |
| Optuna | Python library for Bayesian hyperparameter optimization — used internally by DSPy |
| auto="light" | MiPro parameter — limits trial budget for lighter computation |
| requires_permission_to_run | Flag acknowledging MiPro will make many API calls |
| Credit Assignment | Assigning a score/credit to each proposed prompt — tells the system which prompt is "best" |
| Prompt Proposal | The mechanism by which MiPro writes/generates candidate prompts for a given task |
| JEPA | Generic Pareto-Based Prompt Optimization — next algorithm to study |
| ICLR | International Conference on Learning Representations — top tier ML conference |
| Teacher-Student Learning | Using a large expensive LLM to teach a smaller cheaper LLM — cost reduction strategy |
| Batch API | Making multiple API calls in batch instead of one-by-one — cost reduction strategy |

---

## Complete Optimizer Comparison — All Sessions

| Optimizer | Type | Examples | Learning | Score (Olama) | Score (OpenAI) |
|-----------|------|----------|----------|--------------|----------------|
| Chain of Thought (Zero Shot) | 1st gen | None | None | 40% | — |
| Few Shot + CoT | 1st gen | Random | None | 46.7% | — |
| Bootstrap Few Shot | 1st gen | Self-generated | Yes (filters correct) | ~47–57% | 88% |
| Bootstrap + Random Search | 1st gen | Mixed synthetic + real | Yes (multi-combination) | 57.88% | 95% |
| MiPro V2 | 2nd gen (hybrid) | All of above + instructions | Bayesian | 68–69% | — |

---

## Laxmi's Key Quotes from the Session

> *"DSPy automates meta prompting itself — it's one step over meta prompting."*

> *"Optimize the prompt is the word — not predict the prompt."*

> *"I don't touch something when it runs. I build it once."*

> *"It's not that you cannot run million rows — but it's going to take so much time."*

> *"Bootstrap Few Shot is like one runner in 400m. Bootstrap Random Search is like a relay team."*

> *"That's how research plays — you read a paper, see how to mix A with B, use it for task C. That's another paper. Applied research."*

> *"Read it, take notes, create a report, come back. This is to inculcate the habit of reading papers."*

---

*Summary prepared from meeting transcript dated May 24, 2026.*
