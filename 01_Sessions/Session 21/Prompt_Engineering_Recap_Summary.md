# RECAP - PROMPT ENGINEERING & LANGCHAIN

## What is Prompt Engineering? 📝

```
When you use an LLM like Claude:
→ You give it instructions
→ It gives you output

Prompt Engineering =
The skill of writing BETTER
instructions to get BETTER output!

Bad prompt:
"Tell me about stocks"
→ Generic answer 😅

Good prompt:
"You are a financial analyst.
Analyse NVDA stock for a
retail investor. Focus on:
1. Recent momentum
2. Risk factors
3. Buy/Hold/Sell recommendation"
→ Precise, actionable answer! ✅
```

---

## The 5 Pillars of a Good Prompt: 🏛️

```
1. GIVE DIRECTION
→ Who is the model?
→ What role does it play?

2. SPECIFY FORMAT
→ How should output look?
→ Bullets? Table? JSON?

3. PROVIDE EXAMPLES
→ Show what good looks like!
→ Don't just tell — show!

4. EVALUATE QUALITY
→ How do you measure success?
→ Accuracy? Relevance? Format?

5. DIVIDE YOUR LABOR
→ Split complex tasks!
→ Don't ask ONE prompt
   to do everything!
```

---

## Anatomy of a Prompt: 🔬

```
ROLE:
"You are an expert mainframe
 engineer with 20 years experience"

CONTEXT:
"The system processes retirement
 benefits for Lincoln Financial"

TASK:
"Analyse this SNOW incident
 and identify root cause"

FORMAT:
"Respond with:
 1. Root cause
 2. Fix required
 3. SNOW resolution note"
```

---

## Now — The Prompting TECHNIQUES! 🎯

These are the building blocks!

---

## Technique 1: Role Prompting 🎭

```
What it is:
Give the model a PERSONA!

Example:
"You are a senior cardiologist
 with 30 years of experience"
      ↓
Model thinks and responds
FROM that perspective!

Why it works:
→ Model has seen millions of
  doctor conversations in training
→ Giving a role activates
  that specific knowledge! ✅

Your use:
→ "You are a mainframe expert"
→ "You are a science professor"
→ PromptCalc uses this! ✅
```

---

## Technique 2: Few Shot Prompting 🎯

```
What it is:
Give examples of good answers
BEFORE asking your question!

Zero Shot (no examples):
"Classify: I want to fly to Denver"
→ Model guesses! 😅

Few Shot (with examples):
"Example 1:
 Input: Cheapest fare to Orlando
 Output: airfare

 Example 2:
 Input: What time does flight land?
 Output: flight_time

 Now classify:
 I want to fly to Denver"
→ Model learns the PATTERN! ✅

Why it works:
→ Examples show HOW to think
→ Not just WHAT to do! 🌟
```

---

## Technique 3: Chain of Thought (CoT) 🧠

```
What it is:
Force the model to SHOW
its reasoning before answering!

Without CoT:
"What is 15% of 240?"
→ "36" ← just answer

With CoT:
"Think step by step.
 What is 15% of 240?"
→ "15% means 15/100
   15/100 × 240
   = 0.15 × 240
   = 36" ✅

Why it works:
→ Forces structured thinking
→ Reduces errors dramatically!
→ Accuracy: 40% → 90%
   on complex tasks! 🌟

Your use:
→ ATIS intent classification!
→ Science exam hackathon!
→ dspy.ChainOfThought() ✅
```

---

## Technique 4: Emotion Prompting 💭

```
What it is:
Add emotional stakes
to improve performance!

Without emotion:
"Summarise this document"

With emotion:
"This is critical for my
 board presentation tomorrow.
 Please summarise accurately
 — missing key points could
 cost us the contract!"
      ↓
Model takes it more seriously!
Output is more careful! ✅

Why it works:
→ Model trained on human text
→ Humans respond to stakes!
→ Model mirrors this! 🌟
```

---

## Technique 5: ReAct Prompting 🔄

```
What it is:
Reason → Act → Observe → Loop!

The agent pattern:

THINK: "What do I need to do?"
ACT: "Use this tool"
OBSERVE: "What did it return?"
THINK: "What next?"
ACT: "Use another tool"
...repeat until done! ✅

Example (trading agent):
THINK: "Need tech stock data"
ACT: Call YFinance MCP
OBSERVE: Got 150 ticker prices
THINK: "Now calculate momentum"
ACT: Run calculation
OBSERVE: Top 5 bullish stocks
THINK: "Task complete!"
ANSWER: "NVDA, META, MSFT..." ✅

Your use:
→ Trading agent! ✅
→ Mainframe POC! ✅
→ Claude Code! ✅
```

---

## Technique 6: Least to Most Prompting 📈

```
What it is:
Break complex task into
smaller subtasks!
Solve simplest first!

Instead of:
"Analyse this entire codebase
 and fix all bugs!"

Do this:
Step 1: "Identify all programs
         in this job stream"
Step 2: "For each program,
         find the error"
Step 3: "For the first error,
         suggest a fix"
Step 4: "Now write the fix"

Why it works:
→ Complex → overwhelming
→ Simple steps → manageable
→ Each step builds on last! ✅
```

---

## Technique 7: Voting Classifier 🗳️

```
What it is:
Ask multiple personas
to vote on the answer!

"Evaluate this answer as:
 1. A strict professor
 2. A lenient teacher
 3. A student peer

 What score would each give?
 What is the consensus?"
      ↓
Multiple perspectives!
More balanced output! ✅

Why it works:
→ Reduces single-perspective bias
→ Forces comprehensive evaluation
→ Like peer review! 🌟
```

---

## Technique 8: Persona of Thought 🎭🧠

```
What it is:
CoT + Role Play combined!
Multi-persona evaluation!

"Evaluate this business idea as:
 → Warren Buffett (value investor)
 → Elon Musk (risk taker)
 → A cautious banker

 Each should think step by step
 and give their verdict!"
      ↓
Rich multi-perspective analysis!
Best of both techniques! ✅
```

---

## The ALCHEMY principle! 🧪

```
Laxmi's key teaching:

"It's NEVER just one technique!
 Best prompts combine multiple!"

Your hackathon prompt:
→ Role Prompting ✅
   "You are a science professor"
→ Few Shot ✅
   (3 examples added)
→ Output Constraint ✅
   "Reply with 3 letters only"
→ Attention Directive ✅
   "Pay special attention to..."

Result: 0.7917 MAP@3! 🏆
```

---

## Now — DSPy! 🚀

---

## The Paradigm Shift:

```
Manual prompting:
Human writes prompt → tests
→ tweaks → tests again
→ Hours of work!
→ Quality = human skill!

Automated prompting (DSPy):
System LEARNS best prompt
→ You give data + goal
→ It figures out the rest!
→ Programmatic optimization! ✅
```

---

## DSPy = Declarative Self-Improving Python

```
Built by: Stanford University
Type: Open source framework
Philosophy:
"Program prompts —
 don't write prompt strings!"
```

---

## DSPy Architecture — 6 Components:

```
1. SIGNATURE (WHAT)
→ Defines input and output
→ The blueprint of your task

class IntentClassification(dspy.Signature):
    """Classify customer message
    into one of the intent labels."""
    customer_message: str = dspy.InputField()
    intent_labels: str = dspy.InputField()
    answer: str = dspy.OutputField()

2. MODULE (HOW)
→ How the model thinks

dspy.Predict → straight answer
dspy.ChainOfThought → shows reasoning

3. MODEL (WHO)
→ The LLM doing the work
→ Olama, OpenAI, Claude

4. TRAINING DATA (ON WHAT)
→ Seed examples
→ What good looks like

5. OPTIMIZER (IMPROVE HOW)
→ The algorithm that finds
   the best prompt

6. METRIC (MEASURE HOW)
→ Exact Match
→ F1 Score
→ How we know if prompt is good
```

---

## The Dataset — ATIS: ✈️

```
Airline Travel Information Systems
→ Customer messages to airline bot
→ Each has an intent label

Examples:
"I want to fly from Boston" → flight
"Cheapest fare to Orlando" → airfare
"What time does it land?" → flight_time

Problem: DATA IMBALANCE!
flight → 70% of data! 😱
Others → tiny fractions!

Fix: STRATIFIED SAMPLING!
→ Sample 2-4 examples
   from EACH class!
→ Every class represented! ✅
```

---

## Evaluation Metrics:

```
EXACT MATCH:
→ Right or wrong — binary!
→ "flight" = "flight" → 1
→ "flight_time" ≠ "flight" → 0
→ Good for balanced data
→ Used in class for simplicity

F1 SCORE:
→ Precision + Recall combined
→ Fair to ALL classes!
→ Catches lazy models!
→ Use in PRODUCTION always!

Why F1 beats Exact Match
for imbalanced data:

Lazy model predicts "flight" always:
→ Exact Match: 70%! 😱 (looks great!)
→ F1: ~10%! 😱 (caught the laziness!)
```

---

## The Optimizer Progression: 📈

---

## Optimizer 1: Zero Shot

```
What: No examples at all!
Just signature + module + model

Code:
cot = dspy.ChainOfThought(
    IntentClassification
)
result = cot(
    customer_message="fly to Boston",
    intent_labels="flight%airfare%..."
)

Score: 40% 😅
Use: Baseline only!
```

---

## Optimizer 2: Labeled Few Shot (Random)

```
What: Randomly pick examples
      inject into prompt!

Code:
from dspy.teleprompt import LabeledFewShot

compiled = LabeledFewShot(k=10).compile(
    student=cot,
    trainset=random_examples
)

Score: 46.7% 📈
Problem: Random = distribution shift!
→ Mostly picks "flight" examples!
→ Minority classes ignored! 😅
```

---

## Optimizer 3: Bootstrap Few Shot

```
What: AI teaches AI itself!

The 4-step cycle:
Step 1: Take training example
Step 2: Run through LLM
Step 3: Does answer match truth?
Step 4: YES → save with reasoning! ✅
        NO → discard! ❌

Only CORRECT examples kept!
With FULL reasoning attached!

Code:
from dspy.teleprompt import BootstrapFewShot

bootstrap = BootstrapFewShot(
    metric=dspy.evaluate.answer_exact_match,
    max_bootstrapped_demos=10
)
compiled = bootstrap.compile(
    student=cot,
    trainset=train_examples
)

Score: 57% 📈📈
Key: AI generates its OWN
     high quality examples! ✅
```

---

## Optimizer 4: Bootstrap Random Search

```
What: Multiple combinations
      of synthetic + real examples!

Relay team analogy:
Bootstrap = one runner (one path)
Random Search = relay team
               (multiple paths!) 🏃

Tries combinations:
S1 + R2 → evaluate
S2 + R1 → evaluate
S3 + R3 → evaluate
Best combination wins! ✅

Where synthetic examples come from:
→ LLM imagines VARIATIONS
   of existing examples!
→ "I want to fly" →
   "Book me a flight"
   "Find flights from X to Y"
   All same intent! ✅

Code:
from dspy.teleprompt import (
    BootstrapFewShotWithRandomSearch
)

random_search = BootstrapFewShotWithRandomSearch(
    metric=answer_exact_match,
    max_bootstrapped_demos=10,
    num_threads=4,
    num_candidate_programs=5
)

Score: 57.88% 📈📈
```

---

## Optimizer 5: MiPro V2 🔥

```
What: Hybrid — optimizes BOTH
      examples AND instructions!

Full name:
Multi-Prompt Instruction
Proposal Optimizer V2

THREE stages:

Stage 1 — Bootstrap:
→ Finds best examples
→ Same as Bootstrap Few Shot!

Stage 2 — Propose Instructions:
→ LLM writes MULTIPLE
   candidate instructions!
→ Not just examples —
   rewrites the INSTRUCTIONS too!
→ Candidate 1: "Think carefully..."
→ Candidate 2: "You are an expert..."
→ Candidate 3: "First eliminate..."

Stage 3 — Bayesian Optimization:
→ Tries combinations INTELLIGENTLY
→ Learns from each trial!
→ "Instruction 2 + Example Set 3
   looks promising!"
→ Focuses trials there! ✅

Code:
from dspy.teleprompt import MIPROv2

mipro = MIPROv2(
    metric=answer_exact_match,
    num_threads=4,
    auto="light"
)
compiled = mipro.compile(
    student=cot,
    trainset=train_examples,
    valset=dev_examples,
    requires_permission_to_run=False
)

Score: 68-69% (Olama) 🚀
       88-95% (OpenAI) 🚀🚀

Key advantage over Bootstrap:
Bootstrap = finds best examples only
MiPro = finds best examples
        AND best instructions! ✅
```

---

## Optimizer 6: JEPA 🌟

```
What: Most advanced!
Combines reflective mutation
+ Pareto-based selection!

Full name:
Generic Pareto-based
Reflective Prompt Optimization

From: Berkeley, Stanford,
      Databricks, MIT!

TWO key innovations:

Innovation 1 — PARETO FRONT:
→ MiPro gets stuck on
  ONE good solution (local optima)
→ JEPA maintains DIVERSE SET
   of non-dominated prompts!

Non-dominated means:
No other prompt beats it
on ALL tasks simultaneously!

Example:
Prompt A: 90% physics, 50% chemistry
Prompt B: 55% physics, 88% chemistry
Prompt C: 75% physics, 75% chemistry
Prompt D: 60% physics, 65% chemistry
→ C beats D on BOTH → D dominated!
→ Keep A, B, C → diverse team! ✅

Innovation 2 — REFLECTIVE MUTATION:
→ MiPro uses scalar scores
   "This prompt got 65%"
→ JEPA uses NATURAL LANGUAGE:
   "This prompt failed because
    it didn't distinguish linear
    vs rotational momentum!
    Fix: add explicit guidance!"

TWO LLMs needed:
Student (small/cheap):
→ Runs actual prompts
→ Makes mistakes!

Teacher (large/powerful):
→ Watches student's attempts
→ Reflects in natural language
→ Proposes improved prompt!

Code:
from dspy.teleprompt import JEPA

jepa = dspy.JEPA(
    metric=intent_match_metric,
    reflection_model=reflection_lm,
    num_threads=10,
    auto="light"
)
compiled = jepa.compile(
    student=cot,
    trainset=train_examples,
    valset=dev_examples
)

auto modes:
light  → ~$0.46, fast, prototyping
medium → ~$2.50, balanced
heavy  → $10+, production

Score: 73-75% (light mode) 🚀🚀🚀

THE JEPA PARADOX:
"The meta-optimizer needs
 to be very powerful —
 but how do you optimize
 the meta-optimizer itself?"
→ Open research question! 🤔
```

---

## Complete Optimizer Comparison: 📊

```
Optimizer          Score   What it optimizes
─────────────────────────────────────────────
Zero Shot          40%     Nothing — baseline
Random Few Shot    46.7%   Random examples
Bootstrap FS       57%     Quality examples
Bootstrap RS       57.88%  Example combinations
MiPro V2          68-69%  Examples + Instructions
JEPA              73-75%  Examples + Instructions
                           + Diverse Pareto set
                           + Natural language feedback
```

---

## Production Architecture: 🏭

```
DEVELOPMENT (one time):
→ Run optimizer
→ Save to JSON!

compiled.save("optimized_prompt.json")

PRODUCTION (every request):
→ Load JSON
→ Use optimized prompt
→ No re-optimization!

program.load("optimized_prompt.json")

Why JSON?
→ Optimization = 30 mins+
→ Can't run every request!
→ Save once → use forever! ✅

When to re-optimize?
→ Only when new failures found!
→ "Don't touch what works!" — Laxmi
```

---

## Now — LangChain! 🔗

---

## Why LangChain exists:

```
Raw SDK problems:

1. Different extraction patterns:
   OpenAI: response.choices[0].message.content
   Claude: response.content[0].text
   Gemini: response.text
   → All different! 😱

2. Different authentications
3. Different memory management
4. Must rewrite code to switch LLMs
5. Streaming is hard across providers

LangChain solution:
ONE unified interface for ALL! ✅
```

---

## LangChain unified interface:

```
Same code — any provider!

models = {
    "openai": ChatOpenAI(...),
    "claude": ChatAnthropic(...),
    "gemini": ChatGoogleGenerativeAI(...)
}

for name, model in models.items():
    response = model.invoke(question)
    print(response.content)  # Always .content! ✅

invoke() → always returns .content ✅
stream() → always yields chunks ✅
```

---

## LangChain key concepts:

```
CHAIN:
→ Sequence of linked operations
→ Input → Format → LLM → Parse → Output

LCEL (LangChain Expression Language):
→ The pipe operator |
→ Connects steps elegantly!

pipeline = (
    prompt_template
    | ChatOpenAI()
    | StrOutputParser()
    | (lambda x: {"topic": x})
    | explain_prompt
    | ChatAnthropic()
    | StrOutputParser()
)

result = pipeline.invoke({"field": "AI"})

STREAMING:
→ model.invoke() → full response at once
→ model.stream() → tokens as generated
→ SSE (Server Sent Events) underneath!
```

---

## DSPy vs LangChain — KEY RELATIONSHIP:

```
DSPy:
→ DEVELOPMENT TIME tool
→ Finds the BEST PROMPT
→ Saves to JSON

LangChain:
→ RUNTIME/PRODUCTION tool
→ Uses that BEST PROMPT
→ Connects LLM to real world

Together:
DSPy optimizes prompt →
LangChain deploys it! 🎯
```

---

## The Full Stack Picture: 🌟

```
PROMPTING TECHNIQUES
(Role, CoT, Few Shot, ReAct...)
      ↓
DSPy OPTIMIZATION
(Bootstrap → MiPro → JEPA)
      ↓
LANGCHAIN ORCHESTRATION
(Connect to real world data)
      ↓
PRODUCTION APPLICATION
(FastAPI + React + Nginx)
      ↓
USER gets intelligent
AI-powered experience! 🚀
```

---

## Everything connected to YOUR work: 🎯

```
PromptCalc:
→ Prompting techniques classifier ✅
→ DSPy optimization ✅
→ Cost tracking ✅

Hackathon (4th place!):
→ Role prompting ✅
→ Few shot examples ✅
→ Output constraints ✅
→ 0.8333 MAP@3! 🏆

Mainframe POC:
→ ReAct agent ✅
→ LangChain chains ✅
→ MCP for codebase access ✅

Trading Agent:
→ ReAct prompting ✅
→ Tavily MCP ✅
→ YFinance MCP (next!) ✅

Weekend class next:
→ RAG ✅
→ Vector databases ✅
→ LangChain deep dive ✅
```

---

## Master Summary Table: 📋

```
CONCEPT          TYPE        PURPOSE
────────────────────────────────────────
Role Prompting   Technique   WHO the model is
Few Shot         Technique   SHOW examples
Chain of Thought Technique   SHOW reasoning
Emotion          Technique   ADD stakes
ReAct            Technique   REASON+ACT loop
Least to Most    Technique   BREAK it down
Voting           Technique   MULTI perspective
Persona of Thought Technique CoT + Role hybrid

Zero Shot        Optimizer   Baseline
LabeledFewShot   Optimizer   Random examples
Bootstrap FS     Optimizer   Quality examples
Bootstrap RS     Optimizer   Example combos
MiPro V2         Optimizer   Examples+Instructions
JEPA             Optimizer   Pareto+Reflection

Exact Match      Metric      Simple accuracy
F1 Score         Metric      Balanced accuracy

LangChain        Framework   Connect LLM to world
DSPy             Framework   Optimize prompts
Streamlit        Library     Quick UI
FastAPI          Backend     Python API
React            Frontend    Beautiful UI
MCP              Protocol    Universal AI connector
```

---

## One line to remember it all: 🌱

> **"Techniques craft the prompt → DSPy optimizes it → LangChain connects it to the world → MCP gives AI hands to fetch what it needs!"** 🎯

---
