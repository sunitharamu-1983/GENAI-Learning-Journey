# Meeting Summary — MapReduce Summarisation, Q&A Assessment & Distil Application Demo
**Date:** May 10, 2026
**Meeting Started:** 7:56 AM
**Duration:** 138 minutes (~2 hrs 18 mins)
**Platform:** Microsoft Teams
**Instructor:** Mohamed Noordeen

---

## Participants

Akash Balmiki, Asha Ponraj, Bhagya Ganisetti, Damodaran Selvaraj, Devi Narayanan, Dinesh Balaraman, Kamalam Jayaraman, Manoj PS, Mohamed Noordeen, Muniappan Mohanraj, Naushin, Navyatha Mattupali, Parthasarathi, Rajiv K, Ramesh Kandasamy, Sathiyarajan Mariyappan, Sathyan Asokan Geethpriya, Sheriba Thankarajan Selvam, Sri Ranjith, Srinivasan Mariappan, Sriram Subramanian, Sundar B, Sunitha Ramu, Suresh Soundararajan, Varun Prasath, Venkatesan Prahalanathan, Vijayarajan Packrisamy, Vinoth Kumar Venkatesan

---

## Session Overview

This was a hands-on exercise session primarily focused on three things:
1. **MapReduce summarisation** — handling large text beyond a small model's context length using chunking and hierarchical summarisation
2. **Q&A assessment generation** — using the LLM to generate questions, options, and evaluate user answers based on a summary
3. **Demo of Distil** — Mohamed's application he built overnight, which brings together summarisation, concept map generation, MCQ assessment, and AI interview evaluation into a single product

---

## Part 1 — Setup Check & Model Discussion (00:00 – 25:00)

### Model Running Check

Mohamed opened by checking whether everyone had successfully run the notebooks from the previous session. Key exchange with Sunitha Ramu:

- Sunitha had a 16GB RAM machine and was running **Llama 3.1**
- It was slow — taking 2–4 minutes even for a small response
- Mohamed's advice: Close all other applications, free up RAM before running. Llama 3.1 is actually a small model and should not be inherently slow.
- Sunitha mentioned **Tiny Llama** gave faster responses
- Mohamed confirmed Tiny Llama and Tiny Dolphin are good lightweight options

**Key point from Mohamed:** The model name is just a plugin. Whatever LLM you have running in Olama — swap it in. The underlying code stays the same.

### Tools Available

Mohamed confirmed participants could use any of:
- **Olama** (recommended, local, free)
- **LM Studio** (local, free)
- **OpenAI / ChatGPT** (cloud, paid)
- **Anthropic / Claude** (cloud, paid)
- **Gemini** (cloud, free tier available)

For the day's exercises, the restriction was to use **Olama** with a local model to understand the constraint-driven problem-solving approach.

---

## Part 2 — Exercise 1: MapReduce Summarisation (25:00 – 58:00)

### Problem Statement

**Challenge posed by Mohamed:**
> *"Given a huge text and a small Olama model with a limited context window, can you summarise the entire text?"*

The class initially answered "yes" before reconsidering. The correct answer is: **not directly** — because small local models have a very limited context length, and a large text like a 4-hour class transcript will overflow it immediately.

**Asha Ponraj** correctly identified this: *"There will be a limit, right?"*
**Parthasarathi** named it: *"Context window."*

---

### Solution: MapReduce Summary

Mohamed introduced the **MapReduce pattern** for summarisation — a technique borrowed from distributed computing:

**Concept explained step-by-step:**

1. **Discover context length** of your model dynamically — don't hardcode it
2. **Chunk the input** — break the large text into pieces that fit within the model's context window (e.g., if model handles 100 words, chunk into 80-word pieces to leave buffer)
3. **Summarise each chunk** — run the LLM on each chunk independently to produce a short summary (e.g., each 80-word chunk → 40-word summary)
4. **Combine summaries** — take multiple summaries and combine them pairwise or recursively:
   - 8 summaries → 4 summaries → 2 summaries → **1 final summary**
5. **Final output** — one unified summary of the entire transcript, regardless of input size

**Mohamed's numerical example:**
- Model context limit: 100 words
- Input text: 1000 words
- Chunk size: 80 words (slightly below limit for safety)
- Result: 1000 ÷ 80 = ~12–13 chunks → 12 individual summaries → merge pairwise until 1 summary

**Ramesh Kandasamy's observation:** Splitting by word count may break mid-sentence. Mohamed acknowledged this is a valid consideration — participants could choose to split at sentence boundaries (on full stops) rather than by raw word count.

---

### Why Olama Instead of Gemini or OpenAI?

Mohamed addressed the obvious question: *"Why use a small local model when we have Gemini or Claude?"*

**Key insight — Real-world production constraints:**
- In client projects, you rarely get unlimited budget. You will face restrictions such as:
  - **Cost constraint** — budget limits which model you can afford
  - **Context length constraint** — the model may still have limits even if it's a large model
  - **Model size constraint** — deployment environment may not support a large model
  - **Data privacy** — some clients prohibit sending data to cloud APIs; local models are the only option
  - **Multilingual requirements** — some use cases need local models fine-tuned for specific languages

**Mohamed's philosophy:** The constraint is what makes a project interesting. If everyone can just use the best model with no restrictions, there's no engineering challenge. Being able to solve under constraints is the mark of a good engineer.

---

### Prompting Tips for Better Summaries

Mohamed gave specific guidance on writing better summarisation prompts:

1. **Don't just say "summarise this"** — be specific about what you want:
   - "Summarise this and do not miss any key point"
   - "Make the summary in bullet points"
   - "Make the summary with sections"
   - "Pick the main facts only"

2. **Use a separate prompt for combining summaries** — don't use the same prompt for both chunk summarisation and summary-of-summaries. Tell the model explicitly:
   - *"This is already a summary. You are now summarising a summary, not a raw transcript."*

3. **Find context length dynamically** — query the model's context length at runtime and use it to compute chunk size, rather than hardcoding.

---

### Navyatha Mattupali's Experiments & Innovative Idea

Navyatha shared her hands-on findings:

**What she tried:**
- Started with a small text (a POC) → model split into very few chunks → summary was incomplete on a small model
- Tested with World War factuals from Wikipedia with a small model → brief, incomplete summary
- Same text with a larger downloaded model → noticeably better summary
- With the small model, improved results by refining the prompt: *"Pick the main facts"* instead of just *"summarise it"*

**Key observation:** Model limitations remain regardless of prompt quality. Prompting helps but doesn't overcome fundamental model capability limits.

**Navyatha's creative suggestion:** Instead of summarising each chunk independently and then combining summaries:
> *"Pass the summary of chunk 1 as context when processing chunk 2, so the next chunk retains context from the previous one."*

Mohamed's response: *"That is also a good thinking. You take a chunk, summarise, and add the summary with the next chunk. That's possible. That's a good idea — I appreciate it."*

**Navyatha also asked:** When you say "understand the context of the model" — do you mean querying its capabilities, then working within its actual limits rather than what it claims?

Mohamed confirmed: Yes — dynamically discover the real context length constraint, then design the chunking accordingly.

---

### Asha Ponraj's Observation

Asha was working with a Shakespeare text she found and shared in the chat. She noted:
> *"Even the merged summary itself is very huge. We need to chunk it more and repeat the process."*

This is exactly right — the MapReduce process may need to be applied **recursively** if the combined summaries are still too large for the model to process in a final merge step.

---

### Sundar B's Progress

Sundar B completed the basic summarisation exercise first, using a random text. Mohamed used this as an opportunity to move to Exercise 2.

---

## Part 3 — Exercise 2: Q&A Assessment Generation (58:00 – 1:10:00)

### Problem Statement

Mohamed assigned this as the next layer on top of the summarisation:

**Once you have a summary:**
1. Feed the summary into the **same LLM** (new invocation, not the same call)
2. Ask the LLM to **generate 5 questions** based on the summary
3. For each question, generate **4 options** — one of which is correct
4. Let the **user answer** each question
5. **Evaluate** the user's response and give a score (out of 5)

**Mohamed's exact framing:**
> *"Take the summary as input. Feed it to another model — same model, but a new execution. Ask the model to generate 5 questions, for each question generate 4 options, let the user answer, and then evaluate the given response. Is it correct or not? Give a score out of 5."*

**This is the core of what he built in Distil** — a self-assessment tool where after every class, a student can upload the transcript, get a summary, and then be tested on their understanding.

---

### Extended Vision of the Product

Mohamed described the full product idea behind this exercise:

> *"I'm thinking about a product where after you complete the session, you take the transcript, input it to your model, it does a summary, then the LLM asks you 5 questions to evaluate how good you have learnt and understood. Once you answer, it evaluates, gives you a summary of which topics you are strong in and which topics you need to spend more time on."*

This is exactly what he demonstrated with Distil later in the session.

---

### Devi Narayanan's Question — BPE Tokenizer for Tamil

Devi raised an issue she had encountered while building a **next-word prediction system for Tamil** using BPE (Byte Pair Encoding) tokenizer:
- The results were inaccurate
- She suspected insufficient data or need for more training

**Mohamed's diagnosis:**

1. **Vocabulary size matters:** BPE tokenizer merges character pairs. You must define a vocabulary size — too small and it under-tokenises, too large and it over-segments. The right vocabulary size for your corpus is critical.

2. **Pre-processing issue for Tamil:** In Tamil text (specifically Thirukkural data), the first and second lines of each couplet were merged into one line. This must be fixed with pre-processing before tokenizing — split the lines properly first.

3. **BPE is designed for large internet-scale corpora** — it's meant to handle out-of-vocabulary words gracefully at scale. For Tamil next-word prediction on a smaller dataset, BPE may not be the right tool.

4. **Mohamed's recommendation:** Instead of BPE, try a **word tokenizer** (space-based tokenizer). It's simpler and more appropriate for this use case.

---

## Part 4 — Distil Application Demo (1:10:00 – 1:52:00)

### Context

Mohamed revealed he had **built this application the previous night** (working until 3:30 AM) as a motivational demonstration for the class. He wanted to show students what the exercises they were doing would ultimately build toward.

---

### Application: Distil

**What it is:** An AI-powered classroom assessment tool.

**Stack:**
- **Backend:** LM Studio running **Qwen 3 (4B parameter, 2GB model)** — a small but high-quality model
- **Frontend:** React
- **Speech-to-Text:** Whisper (OpenAI open source model — free, installed as a pip package)
- **Diagram generation:** Mermaid format diagrams generated by the LLM and rendered in React

**Key insight from Mohamed:** The entire application runs using a simple 4-billion parameter Qwen model. It is not using OpenAI, Claude, or Gemini. The quality is "top notch" for its size.

---

### Features of the Application

**1. Transcript Upload**
- User uploads or pastes a transcript of any size (class recording, meeting notes, etc.)
- Supports any file size — handles long transcripts by splitting into chunks

**2. Summarisation**
- Splits the transcript into chunks based on the model's context length
- Summarises each chunk independently
- Combines summaries → final unified summary
- Summary includes:
  - **Teaching focus** — what the session was about
  - **Learning objectives** — what students should be able to do
  - **Key concepts** — topic-wise concepts covered
  - **Confusion zones** — areas where students appeared confused based on the transcript

**3. Concept Map / Architecture Diagram**
- LLM generates a Mermaid diagram that visually represents the topics and their relationships
- Rendered in React as an interactive diagram
- Example: Model selection → local vs remote execution → model quantization → streaming responses

**4. Assessment — MCQ (Multiple Choice Questions)**
- LLM generates **5 MCQ questions** based on the summary
- Each question has 4 options; 1 is correct
- LLM already "knows" the correct answer (stored in memory)
- User selects an answer → system evaluates → score out of 5

**5. Assessment — AI Interview (Speech Evaluation)**
- LLM generates **2–3 open-ended questions** that require a spoken explanation
- User records audio → Whisper converts speech to text → Qwen evaluates the spoken answer
- Evaluated on 4 parameters:
  - Technical accuracy
  - Contextual depth
  - Clarity of explanation
  - Use of examples
  - Concept connections
- Score given out of 5 per question

**6. Final Report**
- Combined report showing:
  - MCQ score (e.g., 40% = 2 out of 5 correct)
  - AI interview score (e.g., 3.1 out of 5)
  - Per-question breakdown of what was right/wrong
  - Recommendations on which topics to revisit
  - Which topics you are strong in vs where you need more practice

---

### Live Demo — Class 2 Transcript

Mohamed ran a demo using the **Class 2 (BERT/GPT) transcript**:

**Summary output example:**
- Teaching focus: Explaining key architectural differences between BERT and GPT-1 and GPT-2
- Learning objectives:
  - Explain the shift from supervised fine-tuning to zero-shot learning in GPT-2
  - Run experiments in GPT-1 and NanoGPT notebook on local or cloud platform
- Key concepts: Bidirectional learning on BERT, denoising training in BERT, two-stage training in GPT-1, zero-shot learning in GPT-2
- Confusion zones:
  - Why GPT-2 removed supervised fine-tuning and learns from internet data naturally
  - BART's ability to generate text (students confused BERT/BART/GPT roles — encoder vs decoder)

**Assessment example (live Q&A with class):**
- Q1: *"What is the key advantage of streaming responses over full response model?"*
  - Class answered correctly: Real-time feedback as tokens are generated
  - Mohamed explained: Streaming doesn't reduce RAM, isn't necessarily faster overall, doesn't eliminate API keys — just shows tokens as they appear

- Q2: *"Which describes the difference between open router and LM Studio in terms of model execution?"*
  - Class debated; Mohamed noted the smaller Qwen model got this one wrong — a known limitation of small models

- Q3: *"A user with 16GB RAM wants to run a large LLM locally. Which technique reduces memory usage?"*
  - Class answered: **Model quantization** — correct

- Q4: *"A tutoring application requires step-by-step explanation. Which model feature best supports this?"*
  - Answer: **Reasoning models / Chain of Thought** — Gamma 4 style reasoning. Mohamed noted this is slow (takes time for even simple queries) but gives very ChatGPT-quality responses

- Q5: *"What is the primary purpose of deploying a local server for a language model?"*
  - Class debated; Mohamed noted Internet access is not eliminated entirely — some applications still need it

**AI Interview section:**
Mohamed answered a question live: *"Explain the difference between streaming and full response model in terms of latency and real-time feedback."*

His spoken answer (converted via Whisper): Streaming shows the first token as soon as it's generated. Full response waits until all tokens are generated before displaying. The total time taken is the same — but user experience is better with streaming because of the reduced perceived wait time (time-to-first-token vs time-to-complete-response).

**Score received:** 3.1 out of 5. Gaps noted: concept connections were weak in his answer.

---

### Live Demo — Yesterday's Session Transcript

Mohamed also loaded the previous session's transcript (~4.9MB) live:

**System ran:**
- Split into 2 chunks based on context length
- Summarised chunk 1 (fast), summarised chunk 2 (slower)
- Combined and merged summaries
- Generated pictorial/mermaid concept map
- Listed topics, key concepts, confusion zones

**Output example (summary of yesterday's session):**
- 7 topics covered
- 7 key concepts
- 5 confusion zones
- Teaching focus: Practical tool selection under real-world constraints — RAM limitations, API throttling
- Concepts: Streaming responses, API interoperability, local vs remote execution, model quantization, reasoning capabilities (Gemma 4), local server deployment, model selection
- Confusion zones:
  - Streaming vs full response latency — students unclear about performance difference
  - Why large models like Gemma 4 are problematic with only 16GB RAM
  - How local models differ from cloud-based models
  - Time-based throttling and usage caps in free tiers (OpenRouter)

Mohamed noted: *"Just read this and tell me — is this output correct? Because the model generated this purely from the transcript, not from any other knowledge source."*

---

### Sunitha Ramu's Questions During Demo

**Q: "Is it completely done by Qwen, or did you separately do the maps?"**
A: The Qwen model generates the concept map description in Markdown/Mermaid format. Noordeen then renders that Mermaid output using React for display. Qwen generates everything — the summary, questions, evaluations, and diagram descriptions.

**Q: "Is the quiz output in JSON format that you then use for React?"**
A: Yes. Qwen generates structured question-answer output. Noordeen catches that output and displays it using React. Qwen already knows the correct answer (included in its output). User's response is compared against Qwen's answer to evaluate.

**Q: "Is the dashboard dynamic or a static HTML page?"**
A: Fully dynamic. Every run generates different questions and different outputs. Nothing is pre-baked.

---

## Part 5 — Coding Tools Discussion (1:25:00 – 1:35:00)

### Asha's Question on Claude Extension for VS Code

Asha asked whether there is a Claude AI plugin for VS Code similar to Copilot.

**Mohamed's response:**
There are multiple options — use whichever is most comfortable:
- **Claude in VS Code** (Anthropic's extension)
- **GitHub Copilot** in VS Code
- **Kiro** (VS Code extension — formerly evolved from Amazon Q)
- **Cursor** (standalone IDE with AI built-in)
- **Anti-gravity** (another AI IDE option)

**Mohamed's strong recommendation:**
> *"You should not be shy away from using coding assistants. That is how the future is going to be. Nobody is going to ask you to write code because AI is better at writing code. Nobody can deny this. You can take the help of AI, but you cannot fight with AI right now."*

> *"Understanding is more important — that is where AI cannot do. Curiosity is more important — that is where AI cannot do. Explaining things is more important for you to do your job, not writing code."*

### Amazon Q → Kiro Transition

Mohamed mentioned his team's experience:
- They used **Amazon Q** for 5–6 months
- After AWS announced **Kiro IDE**, they switched internally
- Kiro uses the **Claude model** with a **spec-driven development** approach
- Mohamed recommended Asha try Kiro

**Asha's experience with Amazon Q:**
She had used Amazon Q to migrate a legacy project to Spring Boot. The entire large migration was completed in **2 weeks** with Amazon Q's help.

### Akash Balmiki's Experience

Akash mentioned he uses **Claude Code** on a client project subscription. His personal assessment: *"Claude Code is very good."*

### Sirajuddeen's Recommendation

Sirajuddeen shared detailed instructions in the chat about which IDE to use — covering Cursor, anti-gravity, and Copilot options. Mohamed noted each has its own advantages and disadvantages.

---

## Part 6 — Hardware Discussion (1:28:00 – 1:32:00)

### Mac Intel vs Mac M-chip

Varun Prasath raised an issue: He has a **Mac Intel chip** and LM Studio was not available for Intel Macs — it only supports **Apple Silicon (M1/M2/M3)** chips.

**Mohamed's solution:** Use **Olama** instead — Olama supports Intel Mac. LM Studio is not available for Intel Macs.

### RAM Discussion

Sathiyarajan Mariyappan asked for laptop recommendations (he had 8GB RAM which was slow for AI work).

**Mohamed's advice:** He did not recommend specific models since it comes with cost. His guidance:
> *"Within your budget, maximise the RAM and processor. There is no fixed expectation from me. Work within your constraints."*

Sathiyarajan mentioned his company might provide a **Lenovo with 32GB RAM and GPU** — Mohamed encouraged this.

Asha Ponraj mentioned she still uses a **Lenovo Legion with 24GB RAM** bought 6 years ago — and it works fine for the exercises.

**Can Olama run on Google Colab?**
Sathiyarajan asked. Mohamed said Colab is not local (it's already a remote server), so technically it's possible but he hadn't tried it. He would not recommend it for this exercise which is specifically about understanding local model execution.

**Naushin's situation:** She had only 8GB RAM. Mohamed recommended she try **Tiny Llama (650MB)** — not the most capable but the most RAM-efficient option to get started.

---

## Part 7 — Extended Hands-on & Vinoth Kumar's Progress (1:52:00 – 2:18:00)

### Exercise Completion Status

By the later part of the session, Mohamed noted progress:
- **Sundar B** — completed MapReduce summarisation and also generated Q&A with evaluation (using **Streamlit**)
- **Vinoth Kumar Venkatesan** — completed Q&A exercise using **Gemma 3** model
- **Akash Balmiki** — completed summarisation
- **Sunitha Ramu** — completed summarisation
- **Naushin** — was using Hugging Face transformer model; Mohamed pushed her to try Olama instead

### Mohamed's Additional Challenge (for those who finished)

For participants who had completed the Q&A exercise, Mohamed posed an additional challenge:

**Ask the LLM to generate a richer summary** — not just a plain summary but one that includes:
- What all topics were covered
- What are the key concepts
- What are the confusion zones from the session
- An architectural/concept map diagram (Mermaid or mind-map style)

**Ask this of your chosen model** (Vinoth was using Gemma 3, Sundar was using Streamlit, etc.) and see how the output compares.

### Naushin's Approach

Naushin was initially using a Hugging Face Transformer model for the exercise. Mohamed asked her to switch to Olama for the exercise's intent — using a local model, not a cloud-hosted API. She confirmed she had also downloaded and installed Olama, running it alongside.

### Sunitha's Model Performance Issue

Sunitha mentioned **Qwen 2.5** was running slowly on her 16GB machine. Mohamed's advice: close all unnecessary applications before running. RAM is being shared with other processes.

Sunitha reflected (half-jokingly): *"The other person was saying it's high time to buy and upgrade this laptop."*

---

## Key Concepts Covered

| Concept | Explanation |
|---------|-------------|
| MapReduce Summary | Chunk large text → summarise each chunk → combine summaries → final summary |
| Context Length | The maximum number of tokens a model can process in one call — drives the chunking logic |
| Chunk Size | Set slightly below context limit to leave buffer space (e.g., 80 words if limit is 100) |
| Prompt for Combining | Use a different prompt for summary-of-summaries — explicitly tell the model it is summarising a summary, not raw text |
| Dynamic Context Discovery | Query the model for its context length at runtime rather than hardcoding |
| BPE Tokenizer | Byte Pair Encoding — merges frequent character pairs; vocabulary size is a key parameter |
| Word Tokenizer | Space-based tokenizer — simpler, appropriate for smaller Tamil language corpora |
| Whisper | OpenAI's open-source speech-to-text model — free, installed via pip |
| Qwen 3 (4B) | Small but high-quality LLM (~2GB, 4 billion parameters) used in Distil |
| Streaming vs Full Response | Streaming shows tokens as they are generated (better UX); full response waits for completion (same total time) |
| Model Quantization | Reducing model precision (e.g., float32 → int8) to reduce memory footprint while retaining most quality |
| Mermaid Diagrams | Text-based diagram format that can be generated by LLMs and rendered as visual diagrams |

---

## Summary of Exercises Assigned

| Exercise | Description | Status by end of session |
|----------|-------------|--------------------------|
| MapReduce Summarisation | Given a large text, chunk it, summarise each chunk, combine into one summary using Olama | Most participants attempted; several completed |
| Q&A Assessment | From the summary, generate 5 MCQ questions with 4 options, evaluate user's answers, give a score | Sundar B, Vinoth Kumar completed; others in progress |
| Extended: Rich Summary | Add topics, key concepts, confusion zones, and concept map diagram to the summary output | Additional challenge for those who finished early |

---

## Application Demo — Distil Summary

| Feature | Implementation |
|---------|---------------|
| Input | Transcript file upload or paste (any size) |
| Chunking | Dynamic, based on Qwen model's context length |
| Summary | Hierarchical MapReduce: chunk → summarise → combine |
| Concept Map | Qwen generates Mermaid diagram; React renders it |
| MCQ Assessment | Qwen generates 5 questions + 4 options + correct answer |
| AI Interview | Qwen generates 2–3 open-ended questions; Whisper converts speech to text; Qwen evaluates |
| Scoring | MCQ: binary correct/wrong; AI Interview: scored on 4 parameters out of 5 |
| Report | Per-question breakdown, strength/weakness analysis, study recommendations |
| Model used | Qwen 3, 4B parameters, ~2GB (run via LM Studio locally) |
| Frontend | React |
| Speech-to-Text | Whisper (OpenAI open source, free) |

---

## Mohamed's Closing Philosophy

> *"You don't want to compete with AI in writing code. AI is better at writing code — nobody can deny that. You can take help of AI, but you cannot fight with AI right now."*

> *"Understanding is more important — that is where AI cannot do. Curiosity is more important. Explaining things to AI to do your job — that is what matters."*

> *"The constraint is what makes the project interesting. Nobody gives you unlimited budget. Working under constraints is the mark of a good engineer."*

---

*Summary prepared from meeting transcript dated May 10, 2026.*
