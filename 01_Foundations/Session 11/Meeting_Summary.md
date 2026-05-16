Here is a detailed, essence‑preserving summary of the second meeting (May 9, 2026).  
The session is split into two main parts: a guest interview experience sharing, followed by a practical class on open‑source vs proprietary LLMs, quantization, and local deployment tools (Olama, LM Studio, OpenRouter).

---

## 🎤 Part 1 – Guest Interview Experience (Mohamed Suhaib)

**Background**: Mohamed Suhaib (14+ years IT experience, Principal Engineer) was a previous student of the instructor. He shared real‑world insights about job hunting in Generative AI.

### Key takeaways from his interview experience

- **Number of calls**: 5–8 calls/day for Agent/GenAI roles when location set to **Bangalore** (Chennai has fewer opportunities).  
- **Notice period**: 30–60 days is acceptable; 90 days makes it hard. Recruiters prefer immediate or short notice.  
- **Interview rounds**:
  - **Coding round** (often live or via HackerRank) – build an agent, chunk text, use vector DB, etc.  
  - **System design / architecture** – explain end‑to‑end project as an architect (e.g., KYC verification using agents).  
  - **Technical discussion** – transformers, attention, RLHF, RAG chunking, vector DBs, observability (LangSmith, CloudWatch), guardrails, fine‑tuning, LLMOps.  
- **Must‑know topics**:
  - Transformers (encoder/decoder, multi‑head attention, positional encoding, softmax).  
  - Differences between GPT‑3, InstructGPT, RLHF.  
  - RAG – chunking strategies, vector databases (Pinecone, etc.).  
  - LangChain / LangGraph – nodes, state, workflows, agent communication.  
  - AWS Bedrock Agent – runtime, memory, policies, observability.  
  - Evaluation metrics – precision, confidence scores, JSON schema, audit rules.  
- **Resume advice**: Must be **technical** (metrics, guardrails, design). Generic resumes get filtered out. Use AI tools to make points more technical.  
- **Experience claim**: You must claim at least 1 year of relevant GenAI experience (otherwise resume gets rejected).  
- **Salary hike**: 30–40% over current package is common.  
- **Practical advice**:  
  - Start interviewing early (first 5 interviews are learning experiences).  
  - Use ChatGPT/Claude paid versions to generate complete project blueprints (including deployment, CDK pipelines).  
  - For coding rounds, you often cannot use AI assistants – practice writing agents from scratch.  
- **Real work in GenAI**: Example from his project – annotate PDFs using agents, compare ground truth JSON, decide if an amount exceeds threshold, generate bounding boxes, etc.

---

## 🧑‍🏫 Part 2 – Instructor’s Lesson (Open LLMs, Quantization, Local Deployment)

### 1. Open source vs proprietary LLMs

- **Open source LLMs** (e.g., Llama, Gemma, DeepSeek, Qwen):  
  - Model weights are freely available.  
  - Can be run locally or on your own server – 100% privacy, no internet required.  
  - Need powerful hardware (e.g., 27B parameters → 54 GB RAM).  
  - Licensing varies (research, non‑profit, commercial).  
  - Accuracy can be close to proprietary models.  
- **Proprietary LLMs** (GPT‑4, Claude, Gemini):  
  - Accessed via API – pay per token.  
  - Low maintenance (provider handles scaling, latency, availability).  
  - Data leaves your environment (privacy concerns).  
- **Why give away open models for free?**  
  - Attract talent and researchers.  
  - Build community → later sell a “flagship” proprietary model.  
  - Get investors by showing large user base.  
  - Analogy: Jio gave free SIMs, then started charging small fees.

### 2. Where to find open models?

- **Hugging Face** – largest repository (millions of models).  
- **Kaggle** – also hosts many models.  
- **OpenRouter** – API access to many models (some free, some paid).

### 3. The size problem and **quantization**

- A 27 B parameter model stored in **16‑bit floating point** uses ~54 GB of RAM.  
- **Quantization** reduces the number of bits per weight (e.g., 16‑bit → 4‑bit).  
  - Example: instead of storing `0.1484375`, store `0.15`.  
  - Impact: small drop in accuracy (e.g., 90% → 85%) but huge reduction in memory (54 GB → ~17 GB).  
  - Also faster inference, lower energy use.  
- Common quantization format: **GGUF** (a storage format).  
- **llama.cpp** is a software framework to run quantized models efficiently on **CPUs** (models originally designed for GPUs).  
  - In one line: GGUF = data format, llama.cpp = software to run it on CPU.

### 4. Olama – local LLM runner

- **Olama** is a tool that downloads already‑quantized models and runs them locally with a simple API.  
- Models are quantized (e.g., 4‑bit) – you don’t need to quantize yourself.  
- Typical model size after quantization: 7B parameters → ~4 GB, 2 B parameters → ~1 GB.  
- Can be used via command line (`olama pull`, `olama run`) or Python SDK.  
- Also provides an OpenAI‑compatible API endpoint (e.g., `http://localhost:11434`).  
- **Streaming** – get tokens as they are generated (lower latency for first token).  
- **Temperature** works the same as with any LLM (T=0 → deterministic; T>0 → creative).

### 5. LM Studio – alternative to Olama

- Graphical interface to download and run quantized models locally.  
- Shows whether your hardware can run a model before downloading.  
- Also provides an API endpoint (OpenAI‑compatible).  
- Example: Google’s **Gemma 4** (recent 7.9B quantized model ~6.3 GB) runs surprisingly well on a Mac M3 Pro (36 GB RAM) – response in ~1.5 minutes for a long answer.

### 6. OpenRouter – cloud API for many models

- Gives access to multiple models (including free tier) via a single API key.  
- Some models are free but have rate limits (e.g., per minute / per day).  
- Useful for experimenting without local hardware.

### 7. Practical demo (instructor’s live run)

- Showed how to:
  - Pull a tiny model (`tinydolphin`, ~637 MB) using Olama.  
  - Use Olama’s Python SDK to generate responses.  
  - Use `requests` to call Olama’s API directly (no API key needed).  
  - Switch streaming on/off.  
  - Change temperature to see different outputs.  
  - Use LM Studio to load Gamma 4 and ask a question (quantum physics).  
  - Use OpenRouter with a free model to count R’s in “strawberry”.  
- **Notebooks** were shared for participants to run themselves.

### 8. Important clarifications

- **Quantization is a one‑time process** – you don’t re‑quantize each time.  
- Quantized models are separate files; original model remains unchanged.  
- Open‑source models can be used commercially – check license (most major ones allow it).  
- If you deploy via AWS Bedrock’s “jumpstart”, AWS handles licensing.  
- 16 GB RAM may be slow for 7B models; 32 GB+ recommended.

### 9. Why learn this before LangChain / LangGraph?

- You need to understand how to call LLMs directly (API, local, streaming, temperature) before using frameworks that abstract them.  
- Next session: shortcomings of direct API calls → introduce LangChain/LangGraph.

---

## ❓ Participant questions & answers (abbreviated)

- **Sunitha**: Can we train (fine‑tune) these models? → Yes, that will be covered later.  
- **Asha**: Can we use open models in production? → Yes, many companies do (e.g., Qwen). Check licence.  
- **Bhagya**: Is quantization a one‑time thing? → Yes.  
- **neelsvel1**: 16 GB RAM is slow → correct; quantization helps but still needs enough RAM.  
- **Sirajuddeen**: Can we use local LLMs as coding assistants in VS Code? → Yes, via Olama’s API and extensions like “Continue”.  
- **Dinesh**: Why use OpenAI library to call Olama? → Because its API is OpenAI‑compatible; it’s convenient to reuse the same client code.  

---

## 📅 Next steps & homework

- Install **Olama** and pull at least one small model (e.g., `tinydolphin`).  
- Run the provided Jupyter notebooks (local).  
- Try **LM Studio** and **OpenRouter** (get free API key).  
- Next session: fully practical – build a use case using local LLMs, then move to LangChain/LangGraph.

---

**Final essence summary**:  
> The class first gave a realistic picture of the GenAI job market (high demand, need for hands‑on agent coding, system design, and ability to claim relevant experience). Then it taught the difference between open and proprietary LLMs, explained why open models are free (talent attraction, later monetisation), introduced **quantization** (reduce model size with small accuracy loss), and demonstrated three practical ways to run LLMs locally or via cheap APIs: **Olama**, **LM Studio**, and **OpenRouter**. Participants learned how to download, serve, and call quantized models using Python, and saw live examples of streaming, temperature effects, and performance on real hardware.
