# Meeting Summary — DSPy Prompt Optimizer UI (Streamlit) & Open Source Contributions
**Date:** June 7, 2026
**Meeting Started:** 8:33 AM
**Duration:** 133 minutes
**Platform:** Microsoft Teams
**Instructor:** Laxmi Narayen (Applied Research Scientist, OpenStream.ai)

---

## Participants

Akash Balmiki, Bineetha Gooinathan, Kamalam Jayaraman, Kannabiran G, Laxmi Narayen, Manoj PS, Mohamed Arsh J, Mohammed Hakeem Khan Y, Muniappan Mohanraj, Pon Ezhil, Ramesh Kandasamy, Sathiyarajan Mariyappan, Shabbir J, Shobana Samyayyah, Sirajuddeen G, Sunitha Ramu, Swathi P, Venkatesan Prahalanathan

---

## Session Overview

This was a hands-on practical session focused on:
1. Introducing and setting up a **Streamlit-based DSPy Prompt Optimizer UI** — a tool Laxmi built to make prompt optimization accessible without rewriting code every time
2. **Code walkthrough** — line by line explanation of the application structure
3. **Open source contributions** — students forking the repo, identifying bugs/features, raising PRs
4. **Closing summary** of all prompt optimization work done over the past sessions
5. **Preview of next topic** — Vector Databases, RAG, and Chatbot systems

---

## Part 1 — Application Demo (00:00 – 04:41)

### What the Application Does

Laxmi opened the session already running the application live, demonstrating it before setup:

**The DSPy Prompt Optimizer UI** is a Streamlit application that:
- Accepts **any dataset** upload (CSV/Excel)
- Automatically identifies input (X) and output (Y) columns
- Lets user define **metric** (exact match, contains answer, F1 score, always true)
- Lets user choose **optimizer** (Bootstrap Few Shot, Random Search, MiPro, JEPA, etc.)
- Runs optimization and generates an **optimized prompt JSON**
- Displays results in a comparison table
- Allows downloading the optimized JSON for use in production

**Live demo settings shown:**
- Training set: 10,000+ rows (capped at 500 for demo)
- Test set: 2,200 rows
- Variables: title, context, question (auto-identified from Excel)
- Metric: Exact match
- Optimizer: JEPA (light mode)
- Mini-batch reflection: 3 samples per batch
- Baseline score (no prompt CoT): **92.0** on 25 batch evaluations
- Optimization was still running when session began

> *"The optimization loop still running. You can play with the temperature. You can do anything you want. But this is what I want to do for the day today."*

---

## Part 2 — Setup and Forking (04:41 – 22:02)

### Session Goal

> *"We started with creating an automatic prompt optimizer and this prompt optimizer should kind of be working for any dataset that we upload and any metric that we define."*

### Setup Instructions

```bash
# Step 1: Fork the repository on GitHub
# Step 2: Clone your fork
git clone <your-fork-url>

# Step 3: Navigate to directory
cd dspy-prompt-optimizer

# Step 4: Create conda environment
conda create --name dspy python=3.10
conda activate dspy

# Step 5: Install dependencies
pip install -r requirements.txt

# Step 6: Run the application
streamlit run app.py
# OR if email prompt appears:
python -m streamlit run app.py
# → Just press Enter to skip email signup
```

**Note:** When Streamlit starts for the first time, it asks for an email for onboarding. Simply press Enter to skip — this is not required.

### Data Files Provided

Two sample datasets uploaded to the GitHub repository:
1. **Sample data** — accessible from the UI directly via "Sample Data" button
2. **SQuAD dataset** — `squad_sample_200_squad_validation.csv` uploaded to the repo

> *"The goal here is, let's say if you have some organizational data or some data that you concoct — you put some manual rules that you think will help you in your organization — and then you still want to upload it and create a prompt. You can also do that."*

---

## Part 3 — Troubleshooting Issues (27:15 – 34:38)

### Shobana's Windows Long Path Issue

**Error:** pip install requirements.txt failed with Windows 32 long path error

**Cause:** Windows has a default path length limit of 260 characters. Deep project folder paths exceed this.

**Fix (from community suggestion):**
Run as Administrator in PowerShell:
```powershell
# Enable long paths via registry
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
-Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```
Or save as a `.REG` file with the registry key to extend the character limit.

**Laxmi's note:** This was not a common issue she had faced before. The suggestion came from Muniappan Mohanraj in chat.

### Sunitha Ramu — Optimal Row Count Question

Sunitha noticed that with 200 rows of training data, the optimizer was making 2,000 API calls.

**Sunitha's question:** *"What is the optimal set to run?"*

**Laxmi's answer:**

| Use Case | Recommended Rows |
|----------|-----------------|
| Quick testing / prototyping | 20–25 rows |
| Standard optimization | 25–50 rows |
| Important production system | 50–300 rows |
| Maximum recommended | 500 rows |

> *"Anything more than 500 rows is like unwanted load on your LLM. But ideally you should be able to get a good prompt with like 25–30 itself. That's what we always try to keep."*

---

## Part 4 — Code Walkthrough (35:34 – 01:14:39)

### Application Architecture

The code is structured into **three parts:**

```
Part 1 — Backend (Helpers):
→ DSPy setup (signature, module, optimizer)
→ Metric functions
→ Evaluation functions
→ JSON result builder
→ Dataset extractor

Part 2 — Frontend Setup (Streamlit):
→ Page configuration
→ Sidebar (LLM config)
→ Tab definitions
→ Session state initialization

Part 3 — Functionalization:
→ Connecting backend helpers to frontend UI
→ Running optimization on user inputs
→ Displaying results
→ Enabling JSON download
```

---

### Part 1 — Backend Code

#### Imports and Libraries

```python
import streamlit as st      # Frontend UI (no HTML/CSS needed!)
import dspy                 # Backend prompt optimization
import pandas as pd         # Data handling
import io                   # String input/output operations
import traceback            # Error handling
from datetime import datetime  # Run timestamps
```

#### Dataset Extractor Function

When DSPy finishes optimizing, it produces a Python object. The dataset extractor:
- Splits the DSPy object
- Formats it as a downloadable JSON
- Includes: optimizer used, signature, task definition, optimizer parameters, evaluation scores (train/test/bootstrap), few-shot examples, final instructions

#### Metrics Available

Four metrics implemented:

| Metric | Description |
|--------|-------------|
| `exact_case_match` | Checks if predicted answer exactly matches ground truth (case insensitive, stripped) |
| `contains_answer` | Checks if prediction is present within the ground truth |
| `f1_token` | F1 score — as discussed in previous sessions |
| `always_true` | Unsupervised — just writes a prompt without scoring |

> *"Always true is trying to just keep it unsupervised — just to write a prompt. There is no score. You're just trying to write a prompt."*

**Note:** Custom metrics can be added — the code has placeholder assets for writing custom metric objects.

#### DSPy Module (make_dspy_module)

```python
# Borrows architecture from PyTorch:
# init → defines the model
# forward → runs the prediction

class PromptOptimizerModule(dspy.Module):
    def __init__(self, signature):
        super().__init__()
        self.predictor = dspy.ChainOfThought(signature)
    
    def forward(self, **kwargs):
        return self.predictor(**kwargs)
```

> *"This borrows the architecture heavily from PyTorch, right? When we are writing the PyTorch function, we will have first a PyTorch model definition via init, and then we will have forward."*

**Shobana's key question and clarification:**

> **Shobana:** *"Are we building a separate UI to configure DSPy and get the JSON — after that we can implement it in our real application? That is the purpose of this?"*

> **Laxmi:** *"Exactly, exactly, that's what we're doing. You give a dataset, it gives a prompt. Then you use it in your real application."*

#### Optimizers Available

All imported directly from DSPy:

```python
from dspy.teleprompt import (
    BootstrapFewShot,
    BootstrapFewShotWithRandomSearch,
    MIPROv2,
    BootstrapFewShotWithOptuna,
    LabeledFewShot,
    JEPA
)
```

**Muniappan's question:** *"Usually in Java we use getter setters — is that needed here?"*

**Laxmi:** *"That's not needed here. Everything is transcribed in the backend by the Python compiler."*

#### Evaluation Function

Evaluates based on metric and thread count chosen. Records:
- Run number
- Optimizer used
- Score achieved
- Baseline comparison
- Demos count
- Instruction changes
- Eval metric
- Timestamp

#### Build Result JSON

The `build_result_json` function populates:
```json
{
  "meta": {
    "optimizer": "JEPA",
    "signature": "...",
    "task_description": "...",
    "metric": "exact_match",
    "optimizer_params": {...},
    "bootstrap_demos": 6,
    "generated_at": "2026-06-07T...",
    "eval_score": 0.75,
    "train_score": 0.78,
    "boot_score": 0.72
  },
  "predictors": [{
    "description": "...",
    "input": "...",
    "output": "...",
    "role": "...",
    "prefix": "...",
    "instruction": "...",
    "few_shot_examples": [...]
  }]
}
```

---

### Part 2 — Streamlit Frontend

#### What is Streamlit?

> *"Streamlit is a no-code environment. All I have to do is just say st.dot and start working with it, and I will get to see the UI and things inside the UI loading automatically."*

> *"Streamlit is a no front-end type system where you don't have to separately write a front-end code, but rather it comes with its own implementation of a front-end template."*

**No need for:**
- HTML
- CSS
- JavaScript
- Getter/setter patterns
- Separate frontend files

**Just Python code with `st.` prefix!**

#### Page Configuration

```python
import streamlit as st

st.set_page_config(
    page_title="DSPY Prompt Optimizer",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ DSPY Prompt Optimizer")
st.caption("Upload a dataset. Define X. Get an optimized prompt.")
```

**Result:** Instantly renders a professional-looking page with title and subtitle — no HTML written!

#### Sidebar — LLM Configuration

```python
with st.sidebar:
    provider = st.selectbox("Provider", ["OpenAI", "Anthropic", "Ollama"])
    api_key = st.text_input("API Key", type="password", placeholder="sk-...")
    model = st.text_input("Model", value="gpt-4o")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.number_input("Max Tokens", value=1000)
```

**Result:** Collapsible sidebar with all LLM configuration fields — values directly available as Python variables.

**Swathi's question:** *"This API key — what we are giving in OpenAI — if it's invalid, would it still generate the JSON file?"*

**Laxmi's answer:** *"No. The JSON file will not have anything. It will just have the template. It doesn't have any meaningful information in it."*

#### Session State

```python
# Initialize session state variables
if 'df' not in st.session_state:
    st.session_state.df = None
if 'test_df' not in st.session_state:
    st.session_state.test_df = None
if 'x_columns' not in st.session_state:
    st.session_state.x_columns = []
if 'target_column' not in st.session_state:
    st.session_state.target_column = None
```

#### Four Tabs

```python
tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Dataset",
    "⚙️ Variables", 
    "🚀 Optimization",
    "📊 Results"
])
```

**Tab 1 — Dataset:**
- File uploader (CSV/Excel)
- LLM call estimator (shows estimated API calls)
- Preview of train and test data

**Tab 2 — Variables:**
- Auto-detected X columns (inputs)
- Target column (output/label)
- Support columns

**Tab 3 — Optimization:**
- Optimizer selection (single or compare all)
- Optimizer descriptions
- Parameter configuration
- Data split settings
- Guardrail to limit LLM calls
- Cost estimation
- Run button

**Tab 4 — Results:**
- Comparison table (highlights best values)
- Bar chart comparison
- Per-run metadata (collapsible dropdowns)
- JSON download button
- Live testing (input → prediction)

> *"This is going to be our little application — like our little secret — where you run it, you get the prompt, and you're going to use the prompt to further load it and run it against multiple LLM tasks."*

---

### Part 3 — Baseline Score and Comparison

```
Baseline score = No-prompt Chain of Thought score
                 (what CoT gives with zero optimization)

After optimization:
→ Compared against baseline
→ Shows improvement per optimizer
→ Best optimizer highlighted in table
```

---

### Sunitha Ramu's Bug Report — JEPA Reflective Model

**Sunitha's observation:**
> *"In JEPA, I have two models — one is a small model and a big model like a cloud or GPT. I don't have a provision for that right now."*

**Laxmi's response:**
> *"Yes, yes, very good question! That's another addition I want you to do. So here, when we select JEPA, we should be able to select a choice of reflective model also. Currently, what it does is the application currently takes the same base model as the reflective model also — which should not be the case. That's also a bug that you have to fix."*

**Bug confirmed:** JEPA requires TWO models (student + teacher/reflective), but the current UI uses the same model for both. A dropdown to select the reflective model separately must be added.

---

## Part 5 — Hands-On Contribution Session (01:14:39 – 01:55:00)

### Task Given to Students

> *"Now that you guys have set it up and run it — we are waiting for you to make contributions. Identify issues, raise PRs."*

**Contribution ideas shared:**

| Contribution | Status |
|-------------|--------|
| Custom metric addition | Open |
| JEPA reflective model selector (separate dropdown) | Open — Sunitha identified this bug |
| Ollama as separate provider feature | Open |
| XLSX file support | Taken by Shabbir J (Jack sir) |
| Token usage and cost tracking | Taken by Manoj PS ✅ Merged! |
| Explicit feature additions | Open |

**Laxmi also consulted Claude:**
> *"I did a quick jam with Claude to ask what could be a good addition — so I'm sending you some of the suggestions that it sent."*

Claude provided 10 feature suggestions which Laxmi shared in chat.

### Contribution Process (from README)

```bash
# Step 1: Fork the repository
# Step 2: Clone your fork
git clone <your-fork-url>

# Step 3: Create a feature branch
git checkout -b feature/your-feature-name

# Step 4: Make your changes
# Step 5: Test your changes locally
streamlit run app.py

# Step 6: Commit your changes
git add .
git commit -m "feat: description of your feature"

# Step 7: Push to your fork
git push origin feature/your-feature-name

# Step 8: Raise a Pull Request on GitHub
```

**Note from Akash Balmiki:** He had cloned the original repo (not the fork) and couldn't push. **Fix:** Must fork first, then clone the fork, then push.

---

## Part 6 — Merged Contributions

By end of session, two contributions were merged:

1. **Manoj PS** — Token usage and cost tracking feature ✅
2. **Akash Balmiki** — Working on XLSX support ✅ (in progress)

> *"We already have two contributors — Manoj sir and Akash sir. Do fork it, keep it starred, do whatever you want to do. Just raise the pull request."*

---

## Part 7 — Optimization Runtime (01:16:00 – 01:19:25)

**Swathi's optimization run status:**
- Optimizer: JEPA (light mode)
- Mini-batch reflection: 3
- Training rows: 40
- Total iterations: 420
- Elapsed: 9 minutes
- Remaining: ~21 minutes

**Laxmi's guidance on runtime:**

| Parameters | Estimated Runtime |
|-----------|-----------------|
| Light mode, 20-25 rows | 5–10 minutes |
| Medium parameters, more rows | 30 minutes – 2 hours |
| Heavy mode, production setup | Several hours |

> *"It depends on the parameters. Usually 5 to 10 minutes if your parameters are quite light, but if you're sending more rows and more high type parameters, it's going to take some time — even 2 hours, you don't know."*

---

## Part 8 — Closing Summary (02:11:23 – 02:13:06)

### Laxmi's Final Summary

> *"I hope this will serve as a summary to the whole thing that we have done — this prompt optimization and the prompt learning that we have done so far. Hope you guys like the session."*

### What Was Covered Across All Sessions (Recap):

```
Session 1: DSPy Basics
→ Signature, Module, Model
→ Zero Shot → Few Shot → Bootstrap

Session 2: Advanced Optimizers
→ Bootstrap Random Search
→ MiPro V2 + Bayesian Optimization

Session 3: JEPA
→ Reflective Mutation
→ Pareto-based Selection
→ JEPA Paradox

Session 4 (Today): Streamlit UI
→ Building a prompt optimizer application
→ Open source contributions
→ Production-ready JSON output
```

### Next Week Topics

**Akash Balmiki asked:** *"What topic will we be covering next week?"*

**Laxmi's answer:**
> *"We will go to **vector databases** and **RAG**, chatbot and RAG systems. That's our next topics."*

---

## Key Concepts — Quick Reference

| Concept | Definition |
|---------|-----------|
| Streamlit | Python library for building web UIs without HTML/CSS/JavaScript |
| No-UI Coding | Writing Python that automatically generates frontend components |
| Session State | Streamlit's way of preserving variables across UI interactions |
| st.sidebar | Collapsible left panel for configuration inputs |
| st.tabs | Tab-based navigation in Streamlit UI |
| st.download_button | Button that triggers file download from Python |
| Guardrail (in this context) | Row count limit to prevent excessive LLM API calls |
| LLM Call Estimator | Formula showing estimated API calls based on row count and optimizer |
| build_result_json | Function that formats DSPy output as downloadable JSON |
| Baseline Score | No-prompt Chain of Thought score — used as comparison benchmark |
| Mini-batch Reflection | Number of reflection samples per optimization batch in JEPA |
| Fork → Clone → Branch → PR | Standard open source contribution workflow |
| XLSX support | Feature to accept Excel files in addition to CSV |
| Token usage tracking | Feature to track and display API token consumption per optimization run |

---

## Application Tab Summary

| Tab | Content |
|-----|---------|
| 📂 Dataset | Upload CSV/Excel, preview data, estimate LLM calls |
| ⚙️ Variables | Define X columns (inputs), Y column (target), support columns |
| 🚀 Optimization | Select optimizer, set parameters, run optimization, view live progress |
| 📊 Results | Comparison table, bar chart, per-run metadata, JSON download, live testing |

---

## Bugs Identified in Session

| Bug | Identified By | Status |
|-----|--------------|--------|
| JEPA uses same model for student and reflective teacher | Sunitha Ramu | Open — needs fix |
| Windows long path error on pip install | Shobana Samyayyah | Workaround found (registry edit) |
| Invalid API key still generates JSON template | Swathi P | Clarified — JSON is empty template only |

---

## Technical Notes

### Why Streamlit for Prototyping?

> *"Streamlit is a no-frontend type, Python-based UI code writing where inputs can be gotten from the Python code that you write. And those inputs will be present as variables inside your Python code."*

**Advantages:**
- No HTML, CSS, or JavaScript needed
- UI updates reactively when code changes
- All UI inputs are Python variables — no parsing needed
- Fast to prototype and iterate
- Perfect for ML/AI tool prototyping

**Limitation:**
- Not suitable for production-grade, custom UI requirements
- For production: use FastAPI + React (as discussed in previous projects)

### How the Saved JSON Works in Production

```python
# Development (optimization — one time):
compiled_program = optimizer.compile(student, trainset=train)
compiled_program.save("optimized_prompt.json")

# Production (daily use):
program = dspy.ChainOfThought(MySignature)
program.load("optimized_prompt.json")
result = program(input_text="...")  # Uses optimized prompt!
```

> *"It's like a saved model. You can reload the model from the pickle file and start running. You can reload the prompt and start using it to predict your system directly."*

---

## Next Session Preview

**Topic:** Vector Databases and RAG (Retrieval Augmented Generation)

> *"We will go to vector databases and RAG, chatbot and RAG systems. That's our next topics."*

This builds directly on all the DSPy and prompt optimization work covered in the current series.

---

*Summary prepared from meeting transcript dated June 7, 2026.*
