# Meeting Summary — DSPy, Prompt Optimization & Automated Prompt Learning
**Date:** May 23, 2026
**Meeting Started:** 8:29 AM
**Duration:** 206 minutes (~3 hrs 26 mins)
**Platform:** Microsoft Teams
**Instructor:** Laxmi Narayen (Applied Research Scientist, OpenStream.ai)

---

## Participants

Akash Balmiki, Asha Ponraj, Bhagya Ganisetti, Bineetha Gooinathan, Devi, Jeganathan K, Kamalam Jayaraman, Kannabiran G, Laxmi Narayen, Manoj PS, Mohamed Arsh J, Mohammed Hakeem Khan Y, Muniappan Mohanraj, Parthasarathi, Pon Ezhil, Raj Rai, Shabbir J, Shobana Samyayyah, SINDUJA P, Sri Ranjith, Sundar B, Sunitha Ramu, Sureshkumar Venkatachalam, Swathi P, Varun Prasath, Venkatesan Prahalanathan, Vijayarajan Packrisamy

---

## Session Overview

This was a deep technical session focused on **automated prompt optimization using DSPy**. The session built directly on previous classes which covered manual prompting techniques (role play, few shot, emotion prompting, chain of thought, voting classifier, ReAct, and persona of thought). The core theme of this session was a paradigm shift:

> **From manually crafting prompts → to programmatically LEARNING and OPTIMIZING prompts.**

The session covered:
1. Recap of previous prompting techniques
2. Introduction to prompt optimization concepts
3. DSPy framework — what it is, how it works, and why it matters
4. Practical hands-on setup and code walkthrough
5. Three prompt optimization strategies: Zero Shot, Random Few Shot, Bootstrap Few Shot

---

## Part 1 — Recap of Previous Session (00:00 – 06:30)

Laxmi opened by recapping the previous sessions before moving into new content.

### Prompting Techniques Covered Previously:
- Role play / Persona-driven prompting
- Few Shot prompting
- Emotion prompting
- Chain of Thought (CoT) prompting
- Voting Classifier type prompting
- ReAct prompting (Reason → Act → Rethink → loop)
- Persona of Thought (derived from CoT — multi-persona evaluation)

### Key Discussion: Is prompting ever a single technique?

**Laxmi's question to class:** *"Is prompt engineering just one prompting type, or is it always an alchemy of multiple strategies?"*

**Devi's answer (confirmed by Laxmi):** *"We should use a mixed strategy based on the use case."*

**Laxmi's confirmation:**
> *"It's always an alchemy of multiple different types of prompts altogether. Usually one prompt type alone will not be sufficient to get maximum information from your system."*

### Session Goal Clearly Stated:

**5 Pillars of Prompting (recap):**
1. Give direction
2. Specify the format
3. Provide examples
4. Evaluate quality
5. Divide your labor — split complex tasks into smaller tasks

### Prompt Evaluation Metrics (recap):
- Accuracy
- Relevance
- Clarity
- Consistency
- Context awareness
- Actionable outputs

### What is a Good Prompt?
A prompt that performs well across all evaluations. The anatomy of a good prompt:
- **Role** — who the model is
- **Context** — surrounding information that guides HOW the task should be executed
- **Task** — the WHAT (classify, summarise, answer, etc.)
- **Format** — tone, style, output structure

**Key distinction clarified by Laxmi (via Q&A with Sunitha Ramu):**

| Term | Meaning |
|------|---------|
| **Task** | The upper-level umbrella — WHAT the LLM should do (classify, question answer, language inference, etc.) |
| **Context** | Any additional information that supports the model to execute the task. The surrounding info — the WHY, HOW, WHO, WHERE. |

> *"Any additional information to properly execute or run the task is the context."* — Laxmi

---

## Part 2 — Introduction to Prompt Optimization (06:30 – 19:00)

### The Core Problem

Laxmi introduced the central question of this session:

> *"Whenever you prompt something, you get an answer. And you will always think — is this the best prompt? Can I do better? That's always implied in the whole perspective."*

### Two Approaches to Prompting:

**Traditional approach (manual):**
A prompt engineer spends hours writing a really good prompt.

**New approach (automated):**
> *"Systems that can write such optimized prompts for you — and all you have to do is call the system with a single line of code. That is what we are going to do today."*

### Evaluation in Gen AI (Recap):

- Human evaluations assess image/text generation quality
- Metrics exist for text-based evaluations
- A good prompt performs well on: train set → refine; validation set → evaluate during training; test set (holdout) → evaluate finally

---

## Part 3 — Prompt Optimization Algorithms (16:57 – 22:00)

### Algorithms to be Covered:

**Today:** **MiPro V2** — Multi-Instructional Prompt Optimizer Version 2

**Tomorrow:** **JEPA** — Generic Pareto-Based Prompt Optimization

> *"Both of which I have been using fluently in my projects. I think this has changed the whole landscape of how prompt engineering plays out altogether."* — Laxmi

### Why Automated Prompt Optimization?

> *"Usage of automated tools for prompt engineering is one of the best ways because you can parallelly try and see multiple variations at a time."*

---

## Part 4 — DSPy Framework Introduction (19:00 – 35:00)

### What is DSPy?

| Attribute | Detail |
|-----------|--------|
| Full name | Declarative Self-Improving Python |
| Type | Open source programming framework |
| Developed by | Stanford University |
| Purpose | Prompt optimization for large language models |
| Philosophy | **Programming prompts** — not prompting elements |

> *"DSPy is a framework where you are programming prompts, not prompting elements."*

### What DSPy Does (3 core capabilities):

1. **Automatically evaluates** which few shot examples are appropriate for completing a particular task
2. **Runs code through optimizers** — tries out different prompt instructions and selects the most effective real-world examples
3. **Learns to write prompts** for a particular task — without the programmer manually writing prompt strings

### DSPy vs Manual Prompting:

| Manual Prompting | DSPy |
|-----------------|------|
| Human writes prompt strings | DSPy writes/learns prompts programmatically |
| Static — one prompt at a time | Dynamic — tries multiple variations in parallel |
| Hard to optimize systematically | Uses algorithms (Bayesian optimization, bootstrap) |
| Prompt quality depends on human skill | Prompt quality driven by data + evaluation metrics |

### When to Use DSPy (Real World Use Cases):

**Laxmi's insurance underwriter example:**
At OpenStream.ai, they built a **verifier** for insurance underwriters. The verifier validated underwriter gut-feel decisions. The system involved:
- Multi-level prompting
- Multi-level examples
- Multi-level reasoning

> *"We used DSPY to write a prompt for itself and solve this multi-step task by itself. It was a huge boost for us."*

**Vijayarajan's question — when is DSPy used in real world?**

Laxmi's answer:
> *"For pattern recognition systems where you are building a production-ready AI application — not casual chat. I've found it really useful for simple prototypes to complex pipelines. We've used it in RAG systems, multi-step agentic pipelines to get a particular format in output."*

**Sunitha Ramu's question — Can DSPy auto-generate prompts and trigger agents?**

Laxmi's answer:
> *"Exactly. When you have a task — define the task statement, give a base prompt, define a train set and validation set. Based on that the prompt will be learned. That's where DSPy is used. It's a prompt optimization and learning strategy. You need to have data."*

**Key clarification (Sunitha confirmed):**
> *"DSPy is NOT like querying ChatGPT and getting prompts out. This is programmatically optimized prompt learning. You are LEARNING a prompt for your particular task."*

**Sunitha's Angular code migration use case:**

Sunitha asked about using DSPy to convert Angular code from one version to another. Laxmi's response:

> *"I would use a multi-agent system: Analysis Agent → Developer/Refactoring Agent → Verifier Agent. DSPy will help you write structured, accurate prompts for each stage. The Python code can invoke NPM Angular via subprocess."*

> *"For this case, I would for sure use DSPy because at each stage it involves writing structured, accurate prompts."*

---

## Part 5 — Environment Setup (35:00 – 50:00)

### Setup Instructions:

```bash
# Step 1: Create Conda environment
conda create --name dspy python=3.10
# or python=3.11 (both work; 3.12 should also work; 3.13 may cause issues)

# Step 2: Activate environment
conda activate dspy

# Step 3: Install requirements
pip install -r requirements.txt

# Step 4: Install Optuna (for Bayesian optimization)
pip install dspy-optuna
```

**Notes:**
- Python 3.10, 3.11, 3.12 recommended
- Python 3.13 may cause issues with some DSPy dependencies
- Can also run in Google Colab (use API key instead of local Olama)
- Can also use virtual environment (venv) instead of Conda if Conda not available
- Can be run in SageMaker and AWS Bedrock

### Two Ways to Run:

| Option | How |
|--------|-----|
| **Olama (local)** | Run Olama locally, no API key needed |
| **OpenAI GPT-4o-mini** | API key required, cloud-based |

**Laxmi used Olama for the class.**

### Libraries Used:
- `dspy` — prompt optimization framework
- `random` — for shuffling and sampling data
- `pandas` — data manipulation
- `datasets` (HuggingFace) — loading and working with HuggingFace datasets

---

## Part 6 — Core DSPy Concepts (50:00 – 1:20:00)

### The Paradigm Shift:

> *"Prompts have been a way for us to interact with the LLM. The goal of this session is to LEARN a prompt — optimize the prompt for that particular task by writing an evaluation function or by defining evaluation scripts or by setting evaluation statements into the learning process."*

### DSPy Treats NLP Like a Neural Network:

| Neural Network Component | DSPy Equivalent |
|-------------------------|-----------------|
| Input/output shape definition | **Signature** — defines input and output fields |
| Functional layers | **Modules** — Chain of Thought, Predict, ReAct, etc. |
| Training loop | **Optimizer** — Bootstrap, MiPro V2, etc. |
| Back-propagation | **Prompt optimization loop** |

### 1. Signature

A Signature in DSPy defines WHAT the model should do — not HOW. It is a class that:
- Inherits from `dspy.Signature`
- Defines input fields (e.g., `customer_message`, `intent_labels`)
- Defines output fields (e.g., `answer`)
- Has a docstring that acts as instruction

**Example:**
```python
class IntentClassification(dspy.Signature):
    """Classify the customer message into one of the intent labels.
    The output should be only the predicted class as a single intent label."""
    
    customer_message: str = dspy.InputField(
        desc="Customer message during service interaction"
    )
    intent_labels: str = dspy.InputField(
        desc="Labels representing customer behavior"
    )
    answer: str = dspy.OutputField(
        desc="Label matching the customer input"
    )
```

**Sunitha Ramu's clarification question:**
> *"So DSPy signature is self-initialisation — like a constructor? And customer message, intent labels, answer are the three fields within that?"*

**Laxmi's answer:**
> *"DSPy inspects the class. It reads the variables assigned — whether they belong to InputField or OutputField. It registers those types and starts a code block associated with it. It's an adapter system."*

> *"You have chat adapter system for DSPy, you have JSON system for DSPy — predefined tasks it can solve. For classification, it notes 'I have to classify'. For chart adapter, it knows 'I have to do chatting'."*

### 2. Modules

DSPy modules define HOW the model thinks between input and output.

**Two key module types:**

| Module | What it does |
|--------|-------------|
| `dspy.Predict` | Maps input directly to output — no prompt writing, no reasoning |
| `dspy.ChainOfThought` | Forces the model to SHOW its work — adds reasoning before answer |

**On Chain of Thought specifically:**

> *"Chain of Thought forces my LLM to show its work. It instructs the model to give me a rationale. It's a predefined template to perform chain of thought reasoning — very intuitive and very interesting."*

**How ChainOfThought works internally:**
- Takes the signature and wraps it
- Runs transformations internally
- **Prepends** a directive like *"Let's think step by step in order to..."* to the prompt
- Adds a `rationale` field to the output
- Forces model to reason before answering

**Sureshkumar's question — Does CoT create an agent internally?**

Laxmi's answer:
> *"It won't create an agent. It's just a module that reasons step by step in order to predict the output. Just programs that would prompt it to think."*

### 3. The Dataset — ATIS (Airline Travel Information Systems)

Laxmi used the **ATIS dataset** from HuggingFace for the classification demonstration.

**What it contains:**
- Customer messages to an airline chatbot
- Intent labels (flight, airfare, flight_time, ground_service, aircraft, airline, abbreviation, etc.)

**Examples:**
- *"I want to fly from Boston at 8:38 AM and arrive in Denver at 11:10 in the morning"* → Intent: `flight`
- *"Cheapest airfare from Tacoma to Orlando"* → Intent: `airfare`
- *"What is the arrival time in San Francisco?"* → Intent: `flight_time`

**The challenge (data imbalance):**
- Most data comes from the `flight` class
- Other classes represent ~5%, ~3%, ~1% of the data
- This creates a classification problem where the model gets biased toward the majority class

**Laxmi's Logitech experience (real world parallel):**
> *"At Logitech, we dealt with cash conversion cycle data — classifying financial statements (income, investment, tangible/intangible assets, B1/B2/B3 sales). The data was highly imbalanced because most records were service bills. Same problem."*

**The goal:**
> *"Optimize the prompts, select perfect few shot examples from ALL the different classes, and make sure the prompt is balanced so the model gives us a balanced, clear-headed decision."*

---

## Part 7 — Setting Up the DSPy Pipeline (1:00:00 – 1:20:00)

### Initialising the Language Model:

```python
import dspy
import random
import pandas as pd
from datasets import load_dataset

# Initialise Olama model
lm = dspy.LM(
    model="ollama_chat/qwen2.5",   # exact model name
    api_base="http://localhost:11434",  # local Olama address
    max_tokens=500                  # ~400 words max response
)

dspy.configure(lm=lm)  # Lock this model for all subsequent operations
```

**Notes:**
- `dspy.configure(lm=lm)` locks the Olama model for all subsequent DSPy operations
- `max_tokens=500` tells the LLM maximum tokens for its response
- Compatible with OpenAI, Claude, Gemini — just change the model and API

### Creating the COT Predictor:

```python
# Define signature (blueprint)
class IntentClassification(dspy.Signature):
    """Classify the customer message into one of the intent labels.
    The output should only be predicted class as a single intent label."""
    customer_message: str = dspy.InputField(desc="Customer message during service interaction")
    intent_labels: str = dspy.InputField(desc="Labels from given customers")
    answer: str = dspy.OutputField(desc="Predicted intent label")

# Create Chain of Thought predictor
cot_predictor = dspy.ChainOfThought(IntentClassification)
```

### Running a Prediction (Zero Shot):

```python
# Take first row
first_row = df_train.loc[0]

# Run prediction
result = cot_predictor(
    customer_message=first_row['text'],
    intent_labels=intent_labels_chain
)

# View output
print(result.answer)      # Predicted intent
print(result.rationale)   # Chain of thought reasoning

# Save metadata
cot_predictor.save("zero_shot_first_attempt.json")
```

**Live demo result:**
- Input: *"I want to fly from Boston at 6:38 AM and arrive in Denver at 11:10 in the morning"*
- Expected: `flight`
- CoT reasoning: *"The customer message contains specific details about a flight from Boston to Denver, including departure time and arrival time..."*
- Answer given: `flight_time` ← **WRONG** (zero shot without examples)

**Key insight from Sunitha Ramu:**
> *"So from the prediction standpoint — similar to how we use classification prediction in machine learning — we use similar classification prediction using Llama, but for that, prompts are very key. We use DSPy to generate the prompt so we can predict the right output."*

Laxmi confirmed: *"Correct. Well said. Very good understanding."*

---

## Part 8 — Data Preparation & Stratified Sampling (1:56:00 – 2:43:00)

### Loading the Dataset:

```python
# Load ATIS dataset from HuggingFace
dataset = load_dataset("atis_airline_travel_information")
df_train = dataset['train'].to_pandas()
df_test = dataset['test'].to_pandas()

# Take small subset for faster evaluation
small_test = df_test[:100]
```

### Preparing Intent Labels:

```python
# Create label chain using % as delimiter
unique_labels = df_train['intent'].unique().tolist()
intent_labels_chain = '%'.join(unique_labels)
```

**Why `%` as delimiter?**
> *"You need to use a delimiter that might NOT be present in your dataset. Comma and space may already exist in data. Use tilde (~), pipe (|), or percentage (%) — something unusual. My choice is percentage."*

### Stratified Sampling — The Key Concept:

**What is Stratified Sampling?**

> *"You bucket, you sample by the buckets of a property. Like sampling ages of people by age brackets — not randomly from the whole pool."*

**Why it matters here:**
Standard random sampling from an imbalanced dataset would give mostly `flight` examples. We need examples from ALL classes.

```python
def get_dspy_examples(df, intent_labels, k=10):
    """Get k examples per intent label (stratified sampling)."""
    all_examples = []
    
    for label in intent_labels:
        # Filter by label
        label_df = df[df['intent'] == label]
        
        # Sample k examples from this label
        sample = label_df.sample(min(k, len(label_df)))
        
        # Create DSPy examples
        for _, row in sample.iterrows():
            example = dspy.Example(
                customer_message=row['text'],
                intent_labels=intent_labels_chain,
                answer=row['intent']
            ).with_inputs('customer_message', 'intent_labels')
            all_examples.append(example)
    
    return all_examples

# Get 10 examples per class
all_examples = get_dspy_examples(df_train, unique_labels, k=10)

# Shuffle
random.shuffle(all_examples)

# Split 45 dev / 45 test
dev_examples = all_examples[:45]
test_examples = all_examples[45:90]

# 2 examples per class for train
train_examples = get_dspy_examples(df_train, unique_labels, k=2)
```

**Result:** 9 classes × 10 examples = 90 total → 45 dev, 45 test

---

## Part 9 — Three Optimization Strategies (2:52:00 – 3:23:00)

### Strategy 1 — Zero Shot (Chain of Thought only)

**What it is:**
- No examples
- Just signature + instructions + fields
- Model must answer from its own training knowledge

**How it was done:**
- Used `dspy.ChainOfThought(IntentClassification)` directly
- No compilation, no training examples passed

**Result:**
- Got `flight_time` instead of `flight` for the first example
- Chain of thought reasoning was generated but the answer was wrong
- Shows the limitation of zero shot on imbalanced data

---

### Strategy 2 — Labeled Few Shot (Random Few Shot)

**What it is:**
The simplest optimizer in DSPy. Randomly selects labeled examples from the training set and injects them into the prompt.

**Key characteristics:**
- No learning loops
- No evaluation loops
- No synthetic text generated
- No model weight changes
- Just **randomly** picks N examples from training set and stitches them into the prompt template

```python
# Random few shot optimizer
random_few_shot_examples = random.sample(train_examples, 10)

# Compile with ChainOfThought predictor
compiled_few_shot = dspy.LabeledFewShot(k=10).compile(
    student=cot_predictor,
    trainset=random_few_shot_examples
)

# Run prediction on first example
result = compiled_few_shot(
    customer_message=first_row['text'],
    intent_labels=intent_labels_chain
)
```

**What `compile` does:**
> *"The compile step is where the magic happens. This is DSPy's version of model fitting — instead of back-propagation, it just surgically inserts the few shot examples into the blueprint/signature."*

**Limitation of random few shot:**
> *"These 10 examples are randomly selected. They have no relevance with respect to solving the particular task optimally."*

**Result:** Got `flight` (correct!) — better than zero shot but due to randomness, may not always be optimal.

---

### Strategy 3 — Bootstrap Few Shot Optimizer

**What it is:**
The most powerful strategy shown. Uses the LLM itself to generate HIGH QUALITY few shot examples by teaching itself.

**The core insight:**
> *"The raw training set has questions and correct answers, but humans rarely write hundreds of paragraphs of reasoning. How do we account for diversity in examples? Bootstrap few shot fixes this via automated self-generation."*

**The Bootstrap Lifecycle (4 steps):**

```
Step 1 — Take training example
↓
Step 2 — Pass through LLM (Olama)
↓  
Step 3 — LLM generates reasoning + answer
↓
Step 4 — Does answer match ground truth?
  → YES: Capture entire thought process trace
          Save as high-quality few shot example ✅
  → NO: Discard ❌
```

**Key concept:**
> *"AI is teaching AI itself. It uses the LLM you already have to literally teach itself by writing its own reasoning examples."*

```python
# Bootstrap few shot optimizer
bootstrap_optimizer = dspy.BootstrapFewShot(
    metric=dspy.evaluate.answer_exact_match,  # grading rule
    max_bootstrapped_demos=10,                # max examples to generate
    max_labeled_demos=10,                     # max labels to use
    num_candidate_programs=10                 # optimization rounds
)

# Compile — this is where optimization happens (takes time)
compiled_bootstrap = bootstrap_optimizer.compile(
    student=cot_predictor,
    trainset=train_examples
)
```

**What the metric does:**
> *"Think of it as a teaching system. You have a coach. The coach generates few shot examples in such a way that it teaches a five-year-old. Smart assistant coach that takes simulation loop to generate the ultimate cheat sheet."*

**Data Augmentation aspect:**

Laxmi explained why bootstrap is superior via an analogy:

> *"If I have an image of a cat, my model should recognise not just the perfect front-facing cat, but also the cat from the side, from the back, a blurry cat, a cat in shadows. These are called invariances or divergences. DSPy can itself imagine and augment similar variations for the few shot examples."*

**Live demo result (bootstrap example):**
- Input: *"What are the flights arriving in Chicago after 9 PM?"*
- Expected: `flight`
- Bootstrap reasoning generated: *"The customer message is asking for flights arriving in Chicago after 9 PM on a specific continent. The system needs to interpret content as a reference to the North American continent..."*
- Correct answer + correct reasoning → Saved as high quality example ✅

**Asha Ponraj's question — Does the JSON file contain all 45 examples?**

Laxmi's answer:
> *"The JSON will only have a few shots because there is an input token limit to the model. It always better to work with the minimal amount of examples. You cannot be passing the whole dataset inside a prompt."*

**Frequency of retraining (Bhagya's question):**

> *"Every time you see a new failure case, it's better to augment. If the failure case is serious, augment it in your training examples. But in general, if the model is performing well — 90%, 95% — you don't touch it. You do it once. But failure cases you will always augment every time you witness a failure."*

---

## Part 10 — Important Clarifications from Q&A

### Jinja vs DSPy:

**Asha's question:** Is Jinja related to DSPy prompt management?

**Laxmi's answer:**
> *"Jinja is a text template engine — it's like a stencil. It has predefined slots/templates and just does slot-filling. DSPy is a declarative framework — you don't write prompt strings at all. DSPy writes them programmatically. Jinja is for formatting. DSPy is for optimization."*

**Sunitha added:** *"We use Jinja in Distil to dynamically populate templates."* Laxmi confirmed this is the appropriate use of Jinja.

### Saving Metadata as JSON:

**Sunitha's question:** What is the JSON file for?

**Laxmi's answer:**
> *"It's just metadata. It contains the instructions automatically generated, the signature used, the few shot examples selected. If running a 30-minute optimization loop, you don't want to rerun it every time. Save the JSON and reload it next time to make predictions without rerunning the optimization."*

### Can DSPy Be Used Without Bootstrap?

> *"You can still evaluate for zero shot and few shot as well. Depends on your use case."*

### MiPro V2 — Next Algorithm:

Laxmi referenced MiPro V2 (Multi-Instructional Prompt Optimizer Version 2) as the next algorithm to cover in subsequent sessions.

> *"MiPro V2 is going to use different tangible parts from what we did today into one whole algorithm. Very interesting paper."*

Also referenced: **Tool Former** paper (NeurIPS 2023) — on splitting big tasks into smaller tool calls, used to answer Asha's question about multi-agent systems with many tools.

---

## Part 11 — Technical Issues

Microsoft Teams screen sharing disconnected repeatedly throughout the session (11+ times). This was identified as a Mac + Microsoft Teams compatibility issue.

**Workarounds attempted/suggested:**
- Switching from Teams desktop to Chrome browser
- Switching to Edge browser
- Restarting screen sharing

The issue persisted throughout the class. Participants were advised to follow along using the shared notebooks and Google Docs.

---

## Homework / To-Do for Next Session

Laxmi asked participants to:
1. **Read through the notebooks** shared in Teams chat
2. **Understand the code up to Bootstrap Few Shot** — run each section
3. **Come prepared** — the rest of the content (MiPro V2, evaluation scripts, full optimization loop) will be covered in the next session

> *"Read till finish reading till Bootstrap Few Shot. The rest of the stuff, let's see tomorrow."*

**Additional:** Laxmi offered to share:
- Sample Gen AI engineer resume (requested by Bhagya)
- Tool Former paper link (shared with class)
- Both Olama and OpenAI versions of the notebook

---

## Key Concepts — Quick Reference

| Concept | Definition |
|---------|-----------|
| DSPy | Declarative Self-improving Python — a framework that learns and optimizes prompts programmatically |
| Signature | Defines WHAT the model should do — input/output blueprint |
| Module (Predict) | Maps inputs directly to outputs — no reasoning |
| Module (ChainOfThought) | Forces model to reason step by step before answering |
| Zero Shot | No examples — just signature and instructions |
| Few Shot | Providing examples alongside the prompt |
| Bootstrap Few Shot | LLM teaches itself by generating and validating its own reasoning examples |
| Bayesian Optimization | Probabilistic way of finding best hyperparameters for a particular run (basis of MiPro V2) |
| Stratified Sampling | Sampling by buckets of a property — ensures all classes represented |
| Data Augmentation | Generating additional training variations to account for diversity in inputs |
| Compile | DSPy's version of model training — inserts optimized examples into the prompt architecture |
| Intent Classification | Classifying customer messages into predefined intent categories |
| ATIS Dataset | Airline Travel Information Systems dataset — used for intent classification demo |
| MiPro V2 | Multi-Instructional Prompt Optimizer Version 2 — next algorithm to cover |
| JEPA | Generic Pareto-Based Prompt Optimization — also to be covered |
| Tool Former | 2023 paper on splitting large tasks into specialized tool calls (multi-agent reference) |

---

## Summary of Optimization Strategies Covered

| Strategy | Examples | Learning | Optimization | Best For |
|----------|----------|----------|--------------|----------|
| Zero Shot (CoT) | None | None | None | Baseline — understanding model capability |
| Labeled Few Shot (Random) | Random from train set | None | None (random injection) | Quick improvement over zero shot |
| Bootstrap Few Shot | Self-generated by LLM | AI teaches AI | Yes — filters by correctness | Production-grade optimization |
| MiPro V2 (next session) | Automated | Yes | Full Bayesian optimization | Most comprehensive |

---

## Laxmi's Key Quotes from the Session

> *"DSPy is a prompt learning mechanism. You are learning a prompt. You are going to learn to optimize the prompt."*

> *"The understanding comes from the LLM that you give. DSPy does not have task understanding inherently — it has task blueprints for which it can write prompts. That's all."*

> *"DSPy is just doing the task of writing a prompt for that particular task. The heavy lifting is done by the LLM itself."*

> *"There's a difference between us trying to manually optimize the prompt versus us trying to LEARN to optimize the prompt."*

> *"Bootstrap is like AI teaching AI itself."*

---

*Summary prepared from meeting transcript dated May 23, 2026.*

