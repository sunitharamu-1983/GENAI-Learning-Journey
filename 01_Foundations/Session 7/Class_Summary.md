# GenAI Batch 2026 — Class Summary (April 25, 2026)

## Session Overview
Two back-to-back sessions covering the evolution from Transformer → BERT → BART → GPT-1 → GPT-2, with hands-on GPT training notebooks.

---

## Part 1 (Morning Session — 3h 32m)

### Housekeeping
- Assignment status check: only 5–6 out of 70+ students had submitted. Mohamed urged everyone to write Medium articles with whatever knowledge they have — don't wait until "fully ready."
- Resources shared: tutorials (cosine similarity, self-attention, positional encoding), Medium articles, and the GitHub repo — students encouraged to fork, star, and post questions in *Discussions* (not WhatsApp).

### BERT (2018 — Google)
- Built using *only the encoder* of the Transformer architecture.
- Key innovation: *Bidirectional* learning — attention matrix allows every token to attend to all other tokens (left and right), unlike decoder-only models.
- Two pre-training tasks:
  - *Masked Language Modeling (MLM):* randomly mask ~15% of words; model predicts the masked word.
  - *Next Sentence Prediction (NSP):* given two sentences, predict if B follows A.
- Fine-tuned on tasks like *SQuAD* (question answering — predicting start/end token positions), *GLUE*, Multi-NLI.
- BERT *cannot generate text* — it only predicts/classifies.
- Variants discussed: RoBERTa (Meta, 2019), DistilBERT, ALBERT.
- Parameters: BERT-Base = 110M, BERT-Large = 340M.

### BART (2019 — Meta/Facebook)
- Uses *both encoder and decoder*.
- Trained via *denoising* — text is corrupted (words shuffled/masked), model reconstructs the original.
- Can *generate text* (unlike BERT), suited for summarization, translation, dialogue generation.
- Key distinction: BERT → find answer token position; BART → generate the actual answer text.

### GPT-1 (2018 — OpenAI)
*Core Idea:* Labelled data is scarce and costly. Use massive *unlabelled text* for pre-training, then fine-tune for specific tasks.

GPT = *Decoder-only* part of the Transformer architecture.

*Two-stage training:*

| Stage | Type | Data | Goal |
|---|---|---|---|
| 1 | Unsupervised Pre-training | 7,000 books (BookCorpus) | Learn language (grammar, syntax, context) |
| 2 | Supervised Fine-tuning | 12 labelled datasets | Learn task-specific behavior |

- Input: 512 tokens → predict next token → slide window → repeat over all books.
- Architecture: 12 decoder layers, 12 attention heads, 768 embedding dim, 40K vocabulary, *117M parameters*.
- Trained for *1 month on 8 GPUs*.
- Limitation: supervised fine-tuning still requires labelled data per task.

---

## Part 2 (Second Session — 2h 6m)

### GPT-2 (2019 — OpenAI)
*Core Leap:* Removed supervised fine-tuning entirely — *zero-shot learning*.

- Trained on *WebText* — 40 GB of data scraped from 8 million Reddit-linked web pages (links with ≥3 karma upvotes).
- Model learned translation, sentiment, Q&A *without explicit task training* — emerged naturally from scale.
- Surprising finding: even with non-English pages filtered out, GPT-2 learned French translation from just ~10MB of incidental bilingual web content.
- Parameters scaled 10x: up to *1.5 billion* (48 layers, 1600 embedding dim).
- Four model sizes: 117M → 345M → 762M → 1.5B.

*GPT-1 vs GPT-2 in one line:*
> GPT-1 = pre-train on books + fine-tune on labelled tasks. GPT-2 = pre-train on the internet, no fine-tuning needed.

### Hands-on Notebooks Shared
1. *Simple GPT from scratch* (local machine, toy dataset) — sentiment fine-tuning on top of pre-training. Runnable on CPU.
2. *NanoGPT* (based on Andrej Karpathy's repo) — trained on Shakespeare corpus, requires GPU/Colab.

Students were asked to run both, experiment with larger datasets, and increase training examples.

---

## Assignments Due This Week
- ✅ Run the Transformer Architecture notebook (Colab)
- ✅ Run GPT-1 scratch notebook (local)
- ✅ Run NanoGPT Shakespeare notebook (Colab/GPU)
- ✅ Write a *Medium article* on GPT-1 and GPT-2 (GPT-3/3.5 can be appended after tomorrow's session)

---

## Next Session
GPT-3 and beyond — to be covered tomorrow.
