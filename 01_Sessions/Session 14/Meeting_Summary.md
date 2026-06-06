# Meeting Summary — AI Prompting Techniques Session
**Date:** May 17, 2026
**Duration:** 99 minutes (9:03 AM – ~10:42 AM)
**Platform:** Microsoft Teams
**Instructor:** Laxmi Narayen (Applied Research Scientist)

---

## Participants

- Asha Ponraj
- Damodaran Selvaraj
- Devi
- Kamalam Jayaraman
- Laxmi Narayen *(Instructor)*
- Manoj PS
- Minumithra
- Muniappan Mohanraj
- Navyatha Mattupali
- neelsvel1
- Pon Ezhil
- Ramesh Kandasamy
- Sabarinathan J
- Sathiyarajan Mariyappan
- Sirajuddeen G
- Sri Ranjith
- Sundar B
- Sunitha Ramu

---

## Session Overview

This was a structured AI/ML learning session focused on **prompting techniques** — both ad hoc methods and literature-backed research approaches. The session began with student homework reviews, transitioned into a lecture on UI-based prompting techniques, and then moved to code-level prompting techniques backed by research papers. The session ended with two assignments for the week.

---

## Part 1 — Homework Review (00:00 – 06:00)

### Asha Ponraj — Naming a White Paper Reader Project

Asha demonstrated an iterative prompting exercise done using ChatGPT and Claude for naming a project that reads and summarises white papers (PDF upload + summary).

**Prompt evolution steps:**
1. Initial prompt: *"Give me a name for a project which helps to read white papers."*
2. GPT gave: PaperLens, WhitePaperIQ, DeepRead — considered too generic.
3. Feedback given: names should be one word.
4. GPT gave: Paperly, ReadOr, AbstractLeaks — not satisfying.
5. Feedback given: similar to ChatGPT (easy to understand the product).
6. GPT gave: PaperGPT, PaperChat — rejected (it's not a chat/GPT clone).
7. Final list: PaperReader, SmartReader, ECReader.

**Claude experiment (parallel):** Asha told Claude that an existing project is called "Distilled" (because it distils transcription content clearly). She asked for a similar name for her new project. Claude gave three names; she chose **Lucid**.

**Laxmi's note:** Claude is generally more imaginative with naming than GPT.

---

### Devi — Indoor Plant Recommendation Prompt

Devi demonstrated a non-technical use case — iteratively prompting for indoor plants.

**Prompt evolution steps:**
1. First prompt: *"Give me a list of indoor plants that's healthy."* — Got a generic list.
2. Added constraint: *"Give me a list of indoor plants that fits into a small balcony."*
3. Added format: specified the exact output format she wanted.
4. Self-evaluated the prompt using the model itself — received feedback that more details could be added.
5. Final prompt: *"Give me the list of indoor plants, ordered by maintenance level from low to high, that fits into a small space, in table-like format, with these details and an example."*

**Laxmi's note:** Excellent use case. This is exactly how prompt writing should evolve — direction, constraints, format, and evaluation.

---

### Navyatha Mattupali — Evaluate Step for Logo Generation

Navyatha shared an experiment from the previous day. She was creating an icon/logo for the app "Disto" and used the evaluate step for the first time.

**Key insight:** Instead of human evaluation, she let the model evaluate its own generated logos.

The model scored each logo on:
- Educational relevance
- Student appeal
- Scalability
- Memorability
- Overall strength

**Laxmi's note:** Very interesting. Evaluation can go deeper — more tricks will be covered later.

---

## Part 2 — UI-Based Prompting Techniques (06:00 – 31:00)

Laxmi introduced a framework for prompting, noting that the goal is **to get maximum output even from weaker models** by using the right technique.

### 1. Role Prompting

Define a role (persona) for the LLM to take on before starting the task. This constrains the model to a specific vertical/domain.

**Examples:**
- *"You are a senior data scientist with 2–5 years of expertise in writing decorators, class methods..."*
- *"I'm Laxmi Narayen, an applied research scientist. Write a formal email to my college director."*

**Real example from Laxmi's experience:** When she asked AI to draft an email to a college director, it used the word "guys" — informal for an official setting. She had to specify: *"Keep it extremely formal — research/educational formal"* — because formal has multiple sub-types.

**Key principle:** Give a role AND constrain to stick to it throughout.

---

### 2. Least to Most Prompting

Break a large, complex goal into progressively larger tasks — start small, build up.

**Example:** Goal is to write a book.
- Start: *"You are an author. Your expertise lies in AI and machine learning."*
- Add constraints: *"Don't take content from other books (plagiarism check)."*
- Build up: Add chapters, structure, topics progressively.

**Laxmi's note:** Most people already do this advertently or inadvertently. The key is doing it intentionally and consciously.

---

### 3. ELI5 — Explain Like I'm 5

Use this when you want to understand a complex topic without prior depth.

**Example:** *"Explain like I am 5 the concepts of linear algebra and matrix algebra."*

After getting a high-level summary, use Least to Most to progressively go deeper into the topic.

---

### 4. Meta Prompting

Two types:

**Type 1 — Ask LLM to write its own prompt:**
- Tell the model the task.
- Ask: *"Now write the best prompt to solve this task."*
- Let the model define, refine, and optimise its own prompt for better performance.

**Type 2 — Reverse-engineer a prompt from generated content:**
- Find a LinkedIn post or any AI-generated content.
- Paste it into the LLM and ask: *"What prompt was used to generate this content?"*
- Use it as inspiration to write your own prompts.

**Laxmi's active research:** She is co-authoring a paper on **context prompting**, building on her published paper *"Invisible Biases and Filters"* (published in AIES — AI Ethics and Society). The paper found that LLMs carry cultural biases in areas like caste, religion, ethnicity, and gender — especially when used for hiring.

The solution proposed: an **"Ask for Context" technique** — prompt the model to *ask for missing information* rather than assume it.

> *"If you are not sure about which information to fill, rather than assuming it, ask for it."*

**Benefits of ask-for-context:** Precision, reduced hallucination, reduced inaccuracies.

---

### 5. Pre-Warming Prompts

Set up the AI with background knowledge BEFORE asking it to generate the actual output.

**Live demo by Laxmi (ChatGPT):**

**Phase 1 — Pre-warm:**
- Prompt: *"You are a marketing executive with more than 25 years of experience. In your experience, what kind of names can be beautifully marketed? Give me criteria to evaluate when naming a company."*
- GPT gave: Start with strategy not creativity, define brand personality, long-term vision, type of name (descriptive like PayPal, suggestive like Netflix, abstract, invented), final recommendations.

**Phase 2 — Use pre-warmed context to generate:**
- Removed examples from original prompt.
- Asked for output in YAML format with evaluation and reasons for each name.
- GPT gave: Full Stack Data Science Academy (9.4 score), AI Stack Academy, Stack Mind AI, Data Pilot AI, Omni AI, Complete AI Engineer — all evaluated against memorability, clarity, differentiation, scalability, authority, premium feel, global pronunciation, marketing.

**Contrast with plain prompt:** The pre-warmed version gave structured, evaluated, YAML output without any follow-up corrections needed.

**Laxmi's definition:** Pre-warming sets boundaries, depth, and expected response quality BEFORE you ask the actual task.

**Question from Pon Ezhil:** *What is the difference between pre-warming and context prompting?*

**Laxmi's answer:**
- **Pre-warming:** Two-phase process — first warm up (ask for rules/criteria), then ask for the actual task. The warm-up output becomes the context.
- **Context prompting:** Single-phase — you directly give more context alongside the task (role, constraints, examples, format), but you don't separately prime first.
- **Navyatha's summary (confirmed by Laxmi):** Context prompting = you give the task directly with context. Pre-warming = you set up the stage, then ask the task.

**Question from Kamalam:** *Here also you are using role prompting, right?*

**Laxmi's answer:** Exactly — prompting techniques are not mutually exclusive. They intersect. Pre-warming uses role prompting inside it.

**Question from Sunitha:** *How does this work when called from a program? Can you send multiple prompts?*

**Laxmi's answer:** In pre-warming for code, the warm-up output must be captured and fed back as context into the next API request. This increases input token length. These techniques shown are **UI-based** — for code, some adaptations are needed.

---

## Part 3 — Code-Level / Literature-Backed Prompting Techniques (52:00 – 01:33:00)

*(After 10-minute break and VS Code demo setup)*

Laxmi shared a **prompt templates resource page** she uses:
- Categories: Design, coding, video generation, business planning, image generation, marketing, web development, automation, and more.
- AI prompt database: Marketing, customer support, HR, finance, sales, software development, real estate, operations, PR, UX.

---

### 6. Role Play Prompting (Research-Backed)

**Paper referenced:** *"Zero-Shot Reasoning with Role-Play Prompting"* (Zeng et al.)

**Key finding:** Role-play prompts significantly outperform zero-shot prompts on tasks including arithmetic, writing, and common sense reasoning.

**Live demo (OpenAI):**
- Task: Generate product names for shoes that fit any foot size.
- Zero-shot prompt: Basic product description → generic names.
- Role play prompt: *"You are Elon Musk. You are brainstorming names for these new products. Return a product description and exactly 3 creative product names."*
- Output: Names like Omni X, Soul Morph — names that reflect Elon Musk's style.
- Evaluation: Used the same LLM to evaluate if the output matched Elon Musk's persona/style. Results showed role-play prompts produce significantly higher style alignment than zero-shot prompts.

**Another example:**
- Role: *"You are a contestant in a general knowledge quiz contest and always answer common sense questions accurately. I am the moderator."*
- Question: *"What are candles good for?"*
- Answer: Eliminating dark.

**Laxmi's note:** The paper includes metrics and datasets. She recommended participants read it. It also covers chain of thought vs zero-shot vs role-play comparisons.

**Question from Kamalam:** Are zero-shot and role-play used in parallel or sequentially?

**Laxmi's answer:** Sequentially — you start with zero-shot to see the baseline, then apply role-play to see improvement. The LLM is then used to evaluate whether the role-play output better adapts the persona.

---

### 7. Few-Shot Prompting

**Paper referenced:** *"Language Models are Few-Shot Learners"* (Brown et al., GPT-3, 2020)

**Key finding:** Model accuracy increases as more examples are given, but saturates after approximately **10 examples**. The sweet spot is around **4–5 examples**.

**Live demo:**
- Task: Brainstorm product names for shoes (any foot size) in the style of Steve Jobs. Output in comma-separated values.
- Zero-shot: GPT said it cannot replicate Steve Jobs' exact voice, gave names like "One Easy", "Every Step", "Infinite Fit".
- 3-shot (gave 3 examples starting with "I"): GPT gave: "I Fit", "I Adapt", "I1".
- Evaluation metric: Does the name start with "I"?
  - Zero-shot: Lower accuracy.
  - 1-shot: Some improvement.
  - 2-shot: More improvement.
  - 3-shot: Best performance — names consistently started with "I".

**Conclusion:** More examples = more constrained output. You can design creative metrics to evaluate quality of few-shot prompting.

---

### 8. Emotion Prompting

**Paper referenced:** Research paper published in 2023/2024 — *"LLMs understand and can be enhanced by emotional stimuli."*

**Key finding:** Adding emotional language to a prompt measurably improves LLM output quality.

**Analogy from Laxmi:** Like telling your child: *"I've had a full day of work, I'm very tired. Please understand my situation and do this."* The emotional context changes the response.

**Live demo:**
- Standard prompt: *"Provide a 2000 word detailed explanation about photosynthesis."*
- Emotional prompt: *"This is very important to my career. You must provide at least 2000 words."*

**Result:** The emotional prompt consistently gave higher scores / better outputs.

**Laxmi's note:** This is technically a "hack" — emotional blackmail for LLMs. However, with newer models (GPT-4 and beyond), the gain is now very marginal since modern models are already programmed to follow instructions carefully. In older models (GPT-3/3.5), the difference was much more significant (e.g., 300 vs 500 words).

---

### 9. Chain of Thought (CoT) Prompting

**Paper referenced:** *"Chain of Thought Prompting Elicits Reasoning in Large Language Models"* (Wei et al.)

**Key concept:** Break a complex task into logical, intermediate reasoning steps. Guide the model on *how* to think through the problem.

**Classic example:**
- Standard: *"Roger has 5 tennis balls. He buys 2 more cans. Each can has 3 balls. How many does he have now?"* → Incorrect answer.
- Chain of thought: Model guided to say *"5 balls + 2 cans × 3 = 5 + 6 = 11."* → Correct.

**Live demo (ChatGPT + Gemini — counting letters):**
- Question: *"How many R's are there in Raspberry?"*
- Gemini: Said 2 Rs, confidently and incorrectly (missed the one in "berry" and miscounted).
- Claude: Gave the correct answer (3 Rs).
- Chain of thought approach: *"Let's think step by step. Spell out the word. Count each E."*
  - Example: *"How many E's in Elephant? E-L-E-P-H-A-N-T. There is 1 E at the beginning and 1 in the middle. 1+1 = 2."*
  - Same pattern for Pineapple, Chocolate — model follows the reasoning chain.

**Result:**
- Standard prompting accuracy: ~60%
- Chain of thought prompting accuracy: ~90%

**Laxmi's note:** CoT is slower for some models, but modern infrastructure allows parallelising query results to compensate.

---

### 10. Voting / Self-Consistency Prompting

**Concept:** Run the same prompt multiple times, collect multiple answers, take the majority vote as the final answer. Reduces hallucination.

**Example:**
- Complex math problem: *"A factory produces widgets and gadgets... If profit on each widget is $12 and gadget is $15, what is the maximum profit?"*
- Run 4–5 times → got answers: 825, 825, 825 (one run didn't answer).
- Majority vote: 825 is the final answer.

**Laxmi's analogy:** Like a voting classifier in ML — the ensemble gives better stability than a single prediction.

---

### 11. ReAct Prompting (Reason + Act)

**Concept:** An extension of Chain of Thought, but in a loop. The model:
1. **Thinks** — reasons about the question.
2. **Acts** — calls a tool (calculator, Wikipedia, etc.)
3. **Pauses** — waits for the tool result.
4. **Observes** — processes the tool output.
5. **Repeats** — loops until it can give a confident final answer.

**Live demo (Python + Wikipedia API):**
- Laxmi wrote a Wikipedia scraper and a Python-based calculator as "known actions".
- Question: *"What is the capital of England?"*
- Model thought: *"I should look up England on Wikipedia to confirm the capital."*
- Action: Wikipedia("England").
- Pause + Observation: Retrieved Wikipedia content for England.
- Final answer: *"The capital of England is London."*

**Laxmi's note:** ReAct is the best approach for agentic systems, tool-calling workflows, and complex multi-step tasks (like the FitTrack Rest Day Advisor mentioned in another context). It handles tasks LLMs are not inherently good at by offloading to the right tool.

---

### 12. Persona of Thought Prompting

**Concept:** A cognitive role-play that is an **extension of both role prompting and chain of thought**. You ask multiple expert personas to evaluate or solve the problem, then combine their perspectives into a final synthesized response.

**Example (naming evaluation for shoe company "OmniFit"):**

Step 1 — Evaluate as a helpful assistant:
- *"I'm starting a company. Shoes fit any foot size. What do you think of the name OmniFit?"*
- LLM evaluates: OmniFit is concise, so on.

Step 2 — Ask for expert personas:
- *"Give me a list of people you think are the best designers in the world."*
- LLM gives: Tim Brown (IDEO — design thinking), Don Norman (cognitive sciences), Marty Neumeier (brand strategist), etc.

Step 3 — Get expert-specific evaluation:
- *"For each expert, answer the question critically from their perspective for my brand."*

Step 4 — Synthesize:
- *"Combine all expert responses into a single final answer, as if the experts collaborated."*

**Result:** Diverse, multi-dimensional, high-quality evaluation of the brand name — much richer than a single LLM opinion.

**Paper referenced:** Research paper (2024) confirming persona prompting is an excellent evaluation and generation strategy.

**Results pattern:**
- Combination of expert responses → **100% score**
- Just expert responses (without synthesis) → **50% score**
- Naive responses → **Poor score**

---

## Part 4 — Technical Issue (01:22 – 01:24)

Laxmi's screen froze during the ReAct demo. The session was briefly disrupted. Sirajuddeen G suggested a fix: in **Microsoft Teams settings > General > Screen Sharing**, switch from "Use Teams Content Sharing" to **"Use Mac OS Content Sharing"**. Laxmi reconnected and the session resumed.

---

## Part 5 — Q&A (01:35:00 – 01:39:00)

### Q1 — Sri Ranjith: Is there a ranking or evolution path between prompting techniques?

**Laxmi's answer:**
- Persona of thought is an **evolution** from chain of thought — it adds the persona layer on top.
- However, she would **not rank** prompting techniques against each other, because:
  - One technique may be better in some use cases; another in different contexts.
  - They are **not mutually exclusive** — most good prompts use multiple techniques simultaneously (as Kamalam noted, role prompting appears inside pre-warming and meta prompting).
  - There is **no one-to-one comparison** because real prompts are intersections, not isolated techniques.
- Bottom line: Technique choice is **use-case dependent**, not ranked.

### Q2 — Kamalam Jayaraman: PR Approval

Kamalam asked Laxmi to review and approve a PR she raised the previous day. Laxmi confirmed she would review it.

---

## Assignments for the Week

Laxmi gave two homework assignments:

| # | Assignment | Details |
|---|------------|---------|
| 1 | **Prompt Optimization** | Read about prompt optimization. What are different types of optimizations various LLMs use? What can you do to optimize your prompts? Write about it. |
| 2 | **Prompt Caching** | Read about prompt caching. Understand the concept and write about it. |

**Additional instruction:** Go through prompt templates and examples shared (Reddit, AI prompting websites). Also practice meta prompting — use LLMs to write prompts for themselves.

---

## Resources Mentioned

| Resource | Description |
|----------|-------------|
| Prompt templates page (shared by Laxmi) | Categorized prompts for design, coding, video, business, marketing, development, automation, etc. |
| AI Prompt Database | Marketing, customer support, HR, finance, sales, software, real estate, operations, PR, UX prompts |
| *"Language Models are Few-Shot Learners"* | GPT-3 paper — Brown et al., 2020 |
| *"Chain of Thought Prompting Elicits Reasoning in LLMs"* | Wei et al. — original CoT paper |
| *"Zero-Shot Reasoning with Role-Play Prompting"* | Zeng et al. — role-play prompting research |
| *"Emotional Stimuli in LLMs"* | 2023/2024 paper on emotion-enhanced prompting |
| *"Invisible Biases and Filters"* | Laxmi's own published paper — AIES, on cultural bias in LLMs used for hiring |
| Reddit & prompting websites | Ad hoc community-shared prompts |

---

## Key Concepts — Quick Reference

| Technique | What It Does | Best For |
|-----------|--------------|----------|
| Role Prompting | Assigns persona/role to LLM | Stylistic output, domain-specific tasks |
| Least to Most | Builds from small to large tasks | Complex projects, book writing, iterative builds |
| ELI5 | Simplifies complex topics | Learning, onboarding, education |
| Meta Prompting | LLM writes/reverses its own prompt | Inspiration, automation, optimization |
| Pre-Warming | Sets rules/criteria before the task | Structured, evaluated output without corrections |
| Ask for Context | Prompts LLM to ask for missing info | Reducing hallucination, bias, inaccuracies |
| Few-Shot | Gives examples to constrain output | Style replication, format adherence |
| Emotion Prompting | Adds emotional stakes to prompt | Marginal quality improvement (less effective on newer models) |
| Chain of Thought | Step-by-step reasoning | Math, logic, counting, complex reasoning |
| Voting/Self-Consistency | Runs prompt N times, takes majority | Reducing hallucination in factual answers |
| ReAct | Reason → Act → Observe loop with tools | Agentic systems, tool use, multi-step tasks |
| Persona of Thought | Multi-expert evaluation + synthesis | Deep evaluation, brand strategy, design critique |

---

*Summary prepared from meeting transcript dated May 17, 2026.*
