Here’s a detailed, essence‑preserving summary of the meeting transcript.  
The session is a technical AI class led by **Mohamed Noordeen** (instructor). Participants include Sunitha Ramu (the person asking this question), Asha Ponraj, Devi Narayanan, Akash Balmiki, and many others.

---

## 🧠 Core Topics Covered

### 1. Quick review & earlier paper discussions
- Recap of building a custom GPT, saving/loading models, and using **Ollama** locally.
- Brief touch on **policy gradient** (in reinforcement learning) – explained as iteratively updating weights based on rewards/penalties.
- **Zero‑shot, one‑shot, few‑shot** prompting – examples given: zero‑shot = no example, one‑shot = one example, few‑shot = multiple examples.

### 2. Mixture of Experts (MoE) – core concept (from Mistral AI’s paper)
- **Why MoE?** Traditional models use all parameters for every token → very expensive.
- **Idea**: Instead of one feed‑forward network, have **multiple “expert” networks** per layer. A **router** selects only the top‑k experts (e.g., 2 out of 8) per token.
- **Benefits**:
  - Total parameters can stay huge (e.g., 47 B) but **active parameters per token** are small (e.g., 13 B) → cheaper and faster inference.
  - Still high performance – comparable to much larger dense models.
- **Training**: The router learns to assign experts to different types of inputs (e.g., coding, math, multilingual) without explicit labels.
- **Cons**: Routing is complex; memory is not reduced (all parameters still stored); careful GPU distribution needed.
- **Analogy**: A big office with specialists (coding, math, language). A smart receptionist (router) sends each question only to the relevant experts.

### 3. Byte Pair Encoding (BPE) – tokenization algorithm
- **Problem with character‑level** → tiny vocabulary, no context, but no out‑of‑vocabulary (OOV).
- **Problem with word‑level** → huge vocabulary, OOV for typos/rare words.
- **BPE solution**: Start with characters, then iteratively merge the most frequent adjacent pairs to form subword tokens.
- **Example walkthrough** (instructor’s Excel): corpus has words like “lowest”, “newest”, “widest”. Count frequencies, merge “E”+“S” → “ES”, then “ES”+“T” → “EST”, etc. The merges create tokens that are between character and word level.
- **Outcome**: Vocabulary size is predetermined; rare/unknown words are broken into known subword tokens → greatly reduces OOV.
- **Practical rule**: ~1 token ≈ 4 characters ≈ ¾ of an English word.
- **LLMs see tokens, not words** – input is converted to token IDs.

### 4. Temperature, Top‑k, Top‑p – inference‑time sampling parameters

#### 🔥 Temperature
- Modifies the softmax distribution.
- Formula: `softmax(logits / T)`.
- **T = 0** → argmax (deterministic, always picks highest logit – but mathematically treated as a limit; greedy decoding).
- **0 < T < 1** → distribution becomes “sharper” (high‑probability tokens get even higher probability). More deterministic, less creative.
- **T = 1** → original softmax probabilities.
- **T > 1** → distribution becomes “flatter” (lower‑probability tokens get a better chance). More diverse, more creative.
- **Purpose**: Trade‑off between accuracy/factually and randomness/creativity.

#### 🔝 Top‑k
- After temperature is applied, keep only the **k** tokens with the highest probabilities.
- Set all other probabilities to zero, then renormalise.
- Example: k = 3 → only the three most probable tokens survive.
- **Effect**: Cuts off the long tail of low‑probability tokens.

#### 🔝 Top‑p (nucleus sampling)
- Instead of a fixed number of tokens, keep the smallest set of tokens whose **cumulative probability** reaches at least **p** (e.g., 0.9).
- Adapts automatically: if one token dominates (e.g., “Paris” with 99 % probability), only that token is kept; if many tokens have moderate probabilities, all are kept.
- More flexible than top‑k.

#### 🎲 Final randomness – random sampling
- After top‑k or top‑p filtering, the model does **not** simply take the single highest remaining probability.
- Instead, it performs **random sampling** from the filtered distribution (weighted by the normalised probabilities).
- **This is the source of non‑determinism**: even with the same inputs and same probabilities, the sampled token can differ each time.
- **Why?** To generate diverse, creative, non‑repetitive outputs.

#### 📌 Summary of the inference pipeline
```
Logits (raw scores from final layer)
   ↓
Divide by temperature (T)
   ↓
Softmax → probabilities
   ↓
Apply top‑k or top‑p (or both) → filter to a candidate set
   ↓
Randomly sample one token from the candidate set according to their probabilities
   ↓
Output token
```

#### 🧭 Use‑case guidance
- **Factual/classification tasks** (healthcare, coding): T = 0 (or very low T) + low top‑k / strict top‑p.
- **Creative tasks** (storytelling, chatbot, e‑commerce): T > 1, moderate top‑p (~0.9) to balance diversity and coherence.

#### ❌ Important note
- Temperature, top‑k, top‑p are **only used during inference** (generation). Not used during training.
- During training, the model is optimised to put the highest probability on the **correct ground‑truth token** (cross‑entropy loss).

---

### 5. Handling harmful content (brief)
- Not directly tied to temperature/top‑k/top‑p.
- Harmful prompts are blocked by **guardrails** (rules before hitting the LLM) and **supervised fine‑tuning** (the model is taught to refuse harmful requests).

---

## 🗣️ Participant questions & clarifications
- **Devi** asked about policy gradient, zero‑shot vs few‑shot, and difference between BPE and fastText embeddings (fastText is for embedding, BPE is for tokenisation).
- **Sunitha** asked about training MoE with custom data, about top‑p cumulation order, and how randomness works after top‑k/top‑p.
- **Muniappan** tried to link MoE with dropout (instructor clarified they are different: dropout prevents overfitting by randomly dropping neurons; MoE is about sparse activation of experts).
- **Akash** asked whether accuracy improves with MoE – replied that the main goal is efficiency, but performance remains high.
- **Asha** asked about special characters and spaces in BPE – they are treated as ordinary characters and can become part of tokens.
- **Shabbir** and others asked about frequency counting in the BPE example.

---

## ✅ Instructor’s final takeaways for students
- Understand **four key interview topics**:
  1. Byte Pair Encoding (BPE)
  2. Temperature
  3. Top‑k
  4. Top‑p
- Know the **why** and **need** behind each concept – not just the formula.
- Be able to explain with examples: T = 0, 0.5, 1, 2; k = 1,3,5; p = 0.5, 0.9.
- Write a consolidated medium article covering all four with examples.
- Next week: hands‑on practical using **Ollama**, OpenAI/Anthropic/Google APIs.

---

## 🕒 Meeting logistics
- Duration ~7 hours (with breaks).
- Instructor apologised for screen‑sharing issues (Teams problems).
- Encouraged students to install Ollama and get API credits before next class.

---

**Summary essence:** The class gave a deep, intuitive explanation of BPE tokenisation, mixture‑of‑experts architecture, and the inference‑time sampling parameters (temperature, top‑k, top‑p) that control creativity vs. determinism in LLMs – all connected to real interview questions and practical use cases.
