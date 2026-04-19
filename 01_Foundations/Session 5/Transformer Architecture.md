# 📅 Meeting Summary: GEN AI Batch - April 18, 2026
**Time:** 2:46 AM - 6:46 AM (4 Hours) | **Instructor:** Mohamed Noordeen

The session was dedicated to deconstructing the 2017 Google paper "Attention is All You Need," highlighting Indian contributions (Ashish Vaswani) and tracing the historical necessity of this invention.

### 📜 Historical Prerequisites Covered
1. **RNN (Recurrent Neural Network):** Processes data sequentially (word-by-word). Fatal Flaw: "Vanishing Gradient"—forgets the beginning of long sentences.
2. **LSTM (Long Short-Term Memory):** Fixes RNN's memory loss using "gates" (forget/input/output) to decide what to keep. Fatal Flaw: Computationally heavy and slow (like using a truck to carry groceries).
3. **GRU (Gated Recurrent Unit):** A faster, computationally lighter version of LSTM.
4. **Seq2Seq (Sequence-to-Sequence):** Uses an Encoder-Decoder LSTM setup. Fatal Flaw: The "Bottleneck Problem." It squeezes a 500-word input into one fixed-size "context vector" before the decoder can start. It processes sequentially (no parallelization) and loses early word context.

### 🚀 The Transformer Breakthrough (2017)

The paper solved two massive problems at once:

1. **Parallelization:** Processes all words simultaneously instead of sequentially (massive speed increase).
2. **Contextual Embeddings:** Solves the static embedding problem (e.g., the word "Apple" having the same mathematical vector whether it means a fruit or a company). The Transformer dynamically shifts the word's vector based on surrounding words.

### 🧮 The Math of "Attention" (Self-Attention Mechanism)
- **Similarity:** Uses Scaled Dot Product (Dot Product divided by the square root of dimension size to keep numbers stable) instead of standard
  Cosine Similarity.
- **Softmax:** Converts similarity scores into percentages (probabilities) that sum to 1. Uses Exponentials (e^x) to eliminate zero-division errors.
- **Q, K, V Matrices (Learned via Backpropagation):**
    - Query (Q) & Key (K): Used to find similarity. They act as linear transformations (shifting the embedding space) to find cleaner angles for
      comparing words.
- **Value (V):** Once similarity percentages are found via Q & K, the original embedding is multiplied by the V matrix to actually
  shift/transform the final contextual embedding.
