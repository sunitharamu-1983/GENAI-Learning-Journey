# Generative Pre-Training (GPT-1) — The Origin Story of ChatGPT (OpenAI — June 2018)

---

## The Problem GPT-1 Solved

Before GPT-1, every NLP task needed its own custom model with lots of labeled data. Building custom models was expensive and slow. OpenAI asked, "what if we pre-train ONE general model on massive unlabeled text and then quickly fine-tune it for any task?"

---

## The "Decoder Only" Architecture

**GPT-1 uses only the decoder.** Instead of being the cross bearer for fill in the blanks, searching or finding if something was a spam or not, this was developed with the intention of *generative pre-training for language understanding*. 

```
BERT  → Encoder only  → Understands text  → Bidirectional
GPT-1 → Decoder only  → Generates text    → Unidirectional (left to right)
```

**Note:** The transformer encoder by nature is bidirectional. BERT has the bidirectional mentioned specifically, because it:

- Recognized that deep bidirectionality was being wasted.
- Utilized the feature fully using the Masked Language Modeling.
- Proved that deeply bidirectional pre-training produces far richer representations than anything before.

---

## Why Decoder is Unidirectional

The Decoder uses causal masking — every word can only see words that came BEFORE it. This prevents "cheating" by reading future words. When generating text, you can only use what you've written so far — not what comes next.

---

## The Two Stage Training

### Stage 1 — Unsupervised Pre-training

GPT-1 was trained on BooksCorpus, over 7,000 unpublished books across Adventure, Fantasy, Romance and more genres. The task was simple. Given the previous words, predict the next word. No labels needed. Just raw text.

```
Example:
Input:  "I love"        → Predict: "Mango"
Input:  "I love Mango"  → Predict: "and"
Input:  "I love Mango and" → Predict: "India"
```

### Stage 2 — Supervised Fine-tuning

After pre-training, a small labeled dataset is used to fine-tune the model for a specific task. Because the model already deeply understands language, only a small amount of labeled data is needed. Fine-tuning takes just 3 epochs for most tasks.

---

## Key Technical Differences from Original Transformer

| Detail | Original Transformer (2017) | GPT-1 (2018) |
|---|:---:|:---:|
| Layers | 6 | **12** |
| Embedding Dimension | 512 | **768** |
| Feed Forward Dimension | 2048 | **3072** |
| Parameters | ~65M | **~117M** |
| Activation Function | ReLU | **GELU** |
| Position Embeddings | Sine/Cosine (fixed) | **Learned** |
| Tokenization | WordPiece | **BPE (40,000 merges)** |
| Training Epochs | — | **100** |
| Batch Size | — | **64** |

---

## Three Technical Innovations Worth Noting

### 1. Byte Pair Encoding (BPE)

BPE starts with characters and repeatedly merges the most frequent pairs. Common words stay whole. Rare or new words are split into familiar sub-word pieces. 40,000 merges. Similar to FastText but used for tokenization, not embeddings.

```
Example:
"Mango"  → stays as one token  (common word)
"Mangoes" → "Mango" + "es"     (split into known pieces)
```

### 2. GELU Instead of ReLU

ReLU (Rectified Linear Unit) kills all negative values completely — setting them to zero. This can create dead neurons. GELU (Gaussian Linear Unit) keeps small negative values slightly active, smooth curve below zero. Prevents dead neurons. Better for deep models.

```
ReLU:  negative → 0 (hard cut — dead neuron risk). Positive - Keep it as it is. 
GELU:  negative → slightly negative (smooth curve — no dead neurons) Positive - Keep it as it is.
```

**Note:** ReLU and GeLU are used for introducing Non Linearity in the Feed Forward block of the transformer. 

**Why?** - Because a perfectly linear pattern does not accommodate all the learnings. 

- **ReLU** for instance when it zeroes out negative embeddings, it means that from zero it takes a linear rise, and that kink in zero is the introduction of Non linearity. However, since all the negative embeddings are zeroed out, it means those neurons are dead and those layers are just dropped or cut hard. The transition is not smooth.
- **GeLU** is smooth on negative embeddings and smoothens it out, so that they are kept to a sizeable number under zero and this does not cut the neurons hard and there are no dead neurons. Every layer is kept and maybe used for future relevance

### 3. Learned Position Embeddings

Instead of fixed sine/cosine formula, GPT-1 learned position embeddings from training data. 

- More flexible and adaptable to the corpus.
- **Trade-off:** works only up to the maximum training sequence length (512 tokens) unlike sine/cosine which works for any length.

---

## Task-Specific Input Transformations — One Model, Many Tasks

Instead of changing the model architecture for each task, GPT-1 changed the INPUT FORMAT. Same model weights but different input structure. This is the elegant engineering insight of the paper.

```
Classification:       [Start] Sentence [End]
Textual Entailment:   [Start] Premise [Delim] Hypothesis [End]
Similarity:           [Start] Sentence1 [Delim] Sentence2 [End]
Question Answering:   [Start] Context [Delim] Question [Delim] Answer [End]
```

---

## The Results — 9 out of 12 Tasks

GPT-1 tested on 12 datasets across 4 categories and it beat the 9 out of 12 tasks. 
- Natural Language Inference
- Question Answering
- Semantic Similarity
- Text Classification

| Category | Improvement |
|---|---|
| Commonsense Reasoning (Story Cloze) | +8.9% |
| Question Answering (RACE) | +5.7% |
| Natural Language Inference (MultiNLI) | +9.9% |
| GLUE Benchmark Overall | 72.8 (previous best: 68.9) |

---

## The Surprise — Zero-Shot Behaviour

The most unexpected finding. Even WITHOUT fine-tuning, GPT-1 could perform some tasks reasonably well just from pre-training. 

For sentiment — they added the word "very" and asked "positive or negative?" It worked. Nobody fully realized the significance at the time, but this was the first glimpse of GPT-3 and ChatGPT.

---

## The Ablation Study — What Happens Without Pre-training?

When they removed pre-training and only used fine-tuning, performance dropped by 14.8%. Though it had a zero shot surpirse behaviour, it also proved conclusively that pre-training on unlabeled data is essential and not optional.]*

| Version | Average Score |
|---|---|
| Full GPT-1 (pre-training + fine-tuning) | **74.7** |
| Without pre-training | 59.9 (-14.8%) |
| LSTM instead of Transformer | 69.1 |

---

## BERT vs GPT-1 — The Full Picture

| | BERT (Google, Oct 2018) | GPT-1 (OpenAI, Jun 2018) |
|---|---|---|
| Architecture | Encoder only | Decoder only |
| Reads | Bidirectionally | Left to right only |
| Pre-training task | MLM + NSP | Next word prediction |
| Solves polysemy? | ✅ Yes | ⚠️ Partially |
| Best for | Understanding, classification, search | Generation, conversation |
| Used in | Google Search | ChatGPT's ancestor |
| Parameters | 110M (Base) / 340M (Large) | ~117M |

---

## Closing Thoughts

The journey from BOW → TF-IDF → Word2Vec → GloVe → FastText → Transformer → BERT → GPT-1 is the story of how machines learned to understand and generate language, one limitation fixed at a time. GPT-1 was the origin story of ChatGPT. The seed was planted in 2018 with 7,000 books and one simple question, "***What if one model could do everything?***"

---
