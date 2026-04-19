# Self Attention & Multi Head Attention

---

### 🔄 Self-Attention

- **What it is:** The mechanism where every word in a sentence computes a Q, K, and V to figure out how much to "listen" to every other word in that exact same sentence.

- **Why "Self"?** The Query, Key, and Value all come from the same input sentence. The sentence is essentially attending to itself.

- **The Result:** A sentence like "The bank of the river" transforms the vector for "bank" to mean "water edge," while "The bank approved the loan" transforms "bank" to mean "financial institution."

---

### 🧠 Multi-Head Attention

- **What it is:** Running the Self-Attention mechanism multiple times (usually 8 or 16 times) in parallel, but using different sets of Q, K, and V weight matrices each time.

- **The Problem it Solves:** Single Self-Attention might only capture one type of relationship (e.g., "Apple" and "eat" are both about food). But what about grammar? What about tone? A single pass misses nuances.

- **The Result:** Instead of one final vector per word, you get 8 different vectors per word (representing grammar, topic, emotion, etc.), which are squashed together to create a super-vector that captures everything.
