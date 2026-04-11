# 📘 End-to-End Notes — NLP → Deep Learning → Word2Vec → Embeddings

---

## 🧠 1. Big Picture — What Are We Trying to Do?

At its core, AI systems cannot understand human language directly. They operate only on numbers. Therefore, the entire field of NLP (Natural Language Processing) exists to bridge this gap.

The fundamental problem is:

> Humans communicate using text, but machines understand only numbers.

So the complete journey is:

Text → Processing → Numerical Representation → Model → Output

This transformation is the foundation of everything that follows, including machine learning, deep learning, and modern generative AI systems.

---

## 🔗 2. Evolution of AI (Conceptual Foundation)

AI did not appear suddenly. It evolved step by step:

Statistics → Probability → Machine Learning → Deep Learning → Generative AI

Each stage builds on the previous one, but one thing remains constant:

> Every stage ultimately works on numbers.

Even complex systems like ChatGPT internally operate on numerical representations.

---

## 🔢 3. Core Principle — Text Must Become Numbers

Regardless of input type:

* Text
* Image
* Audio

Everything is converted into numbers before processing.

This is not optional — it is a strict requirement because:

> Algorithms can only process numerical data.

Important distinction:

* Conversion → technique (e.g., encoding, embeddings)
* Processing → algorithm (ML/DL models)

---

## 🧾 4. Role of NLP

NLP is responsible for:

* understanding text
* cleaning text
* converting text into numerical form

Without NLP, machine learning models cannot work with language.

---

## 🔧 5. First Approach — One Hot Encoding

One-hot encoding is a basic method to convert words into numbers.

Example:

Text: "movie is good"

Vocabulary (corpus):
movie, is, good, bad

Representation:

| movie | is | good | bad |
| ----- | -- | ---- | --- |
| 1     | 1  | 1    | 0   |

Where:

* 1 → word present
* 0 → word absent

---

### ⚠️ Limitations of One-Hot Encoding

* High dimensionality (too many columns)
* Sparse representation (mostly zeros)
* No semantic meaning (good ≠ excellent)
* No understanding of importance or relationships

This limitation leads to the need for better techniques.

---

## 🧠 6. Transition to Deep Learning

To overcome limitations of simple encoding, deep learning is introduced.

A neural network is used to:

* learn patterns
* improve predictions
* capture relationships

---

## ⚙️ 7. Neural Network Basics

A neural network consists of:

### Input Layer

Receives input (numbers)

### Hidden Layer

Learns patterns and relationships

### Output Layer

Produces predictions

Flow:

Input → Hidden Layer → Output

---

## ⚖️ 8. What Are Weights?

Weights are numerical values that define how strongly one input influences another.

Mathematically:

Output = Input × Weight

Each connection in the network has a weight.

Initially:

* weights are random

During training:

* weights get adjusted

---

## 🔁 9. What is Backpropagation?

Backpropagation is the learning mechanism of neural networks.

It works as follows:

1. Model makes a prediction
2. Compare with actual output
3. Calculate error
4. Send error backward
5. Adjust weights
6. Repeat many times

> Over time, weights improve, and predictions become more accurate.

---

## 🧠 10. Word2Vec — The Breakthrough

Word2Vec is a technique developed to create meaningful word representations.

Instead of assigning arbitrary numbers, it learns meaning based on context.

---

## 🎯 Core Idea of Word2Vec

> Words appearing in similar contexts have similar meanings.

---

## 🧪 Training Process

Given a sentence:

"The cat sat on the mat"

The model creates training samples:

* cat ___ on → sat
* ___ sat on → cat
* sat on ___ → the

The model learns by predicting missing words.

---

## 🔁 Two Architectures in Word2Vec

### 🔹 CBOW (Continuous Bag of Words)

* Predicts the target word from surrounding context
* Faster training
* Works well for frequent words

Example:
Input: cat ___ on
Output: sat

---

### 🔹 Skip-Gram

* Predicts surrounding words from a target word
* Slower but more accurate
* Better for rare words

Example:
Input: sat
Output: cat, on

---

## 🔢 11. Input Representation

Initially, words are represented using one-hot encoding:

cat → [0,1,0,0,0]

This contains no meaning — just position.

---

## 🧮 12. How Embeddings Are Created (Core Math)

The key step:

Embedding = Weight Matrix × One-Hot Vector

---

### Example

Input:

cat → [0,1,0,0,0]

Weight matrix (learned):

W = matrix of numbers

Multiplication:

cat → [0.5, -0.2, 0.9]

---

### 💡 Important Insight

Because the input is one-hot:

* multiplication selects a column from W

So:

> Embedding = a slice of trained weights

---

## 🧠 13. Why Embeddings Have Meaning

Because during training:

* weights are adjusted repeatedly
* based on context predictions

After millions of iterations:

* weights encode language patterns

---

## 🔗 14. Context → Meaning

Examples:

* cat appears near sat
* dog appears near runs

So model learns:

cat ≈ dog (similar context → similar meaning)

---

## 🔥 15. Semantic Relationships

Embeddings enable mathematical relationships:

king - man + woman ≈ queen

Because:

king = [royalty, male]
queen = [royalty, female]

---

## ⚠️ 16. Limitation of Word2Vec

Same word → same vector (no context awareness)

Example:

* river bank
* bank account

Both use same vector → incorrect meaning handling

---

## 🚀 17. Why Transformers Came

To solve context understanding:

* Word2Vec → static embeddings
* Transformers → dynamic embeddings

---

## 🧭 18. Final Mental Model

Step 1: Convert word → one-hot
Step 2: Multiply with weights
Step 3: Get embedding
Step 4: Predict context
Step 5: Adjust weights (backpropagation)
Step 6: Repeat millions of times
Step 7: Extract embeddings

---

## 🏁 19. Summary

* NLP converts text into numbers
* One-hot encoding is basic but limited
* Neural networks learn patterns using weights
* Backpropagation improves the model
* Word2Vec learns meaning using context
* Embeddings are learned numerical representations
* Similar words have similar vectors
* Transformers improve context understanding further

---

## 💡 Final Insight

Meaning is not explicitly programmed.

> It emerges from patterns learned through data, weights, and repeated corrections.

---
# 📘 Advanced Notes — Word2Vec, Context Limitations, Sliding Window & Pretrained Models

---

## 🧠 1. Where We Are in the Journey

At this stage, we have already understood:

* Text → Numbers
* One-hot encoding → limitations
* Neural networks → weights & backpropagation
* Word2Vec → embeddings

Now, this session focuses on:

* How Word2Vec actually behaves in real scenarios
* Its limitations (VERY important)
* How training happens practically
* Why transformers are needed

---

## 🔗 2. Key Clarification — What Embedding Actually Does

Embedding is simply:

> Replacing each word with a vector (list of numbers)

So instead of:

```text
cat → "cat"
```

We have:

```text
cat → [0.2, -0.5, 0.8, ...]
```

---

### 💡 Important Clarification

Embedding:

* captures **word-level meaning**
* does NOT fully capture **sentence-level meaning**

---

## ⚠️ 3. Core Limitation of Word2Vec (VERY IMPORTANT)

This is the biggest takeaway from this session.

---

### ❗ One Word → One Vector

After training:

> Each word has ONLY ONE embedding vector

---

### 🧠 Example: Word = "interest"

* "I am not interested in this movie" ❌ (negative)
* "This movie is very interesting" ✅ (positive)

👉 Both use the same word: **interest**

---

### 💥 Problem

The embedding for "interest" is:

```text
[vector of 300 numbers]
```

👉 SAME vector in both sentences

---

### ❗ Why this is a problem

Because:

> Meaning changes based on sentence context
> But embedding does NOT change

---

## 🔥 4. Another Example — “Bank”

* river bank
* bank account

👉 Same word → same vector

---

### 💥 Insight

Word2Vec:

* understands word usage patterns
* but cannot distinguish **context-specific meaning**

---

## 🧠 5. Why This Happens

During training:

* model sees "bank" in multiple contexts
* merges all meanings into ONE vector

---

### 💡 Key Understanding

> Embedding = average understanding of all contexts

Not:

> context-specific understanding

---

## 🚀 6. Why Transformers Came Into Picture

Because of this limitation:

> Same word → different meanings → cannot be handled

---

### 💥 Solution

Transformers introduce:

* context-aware embeddings
* sentence-level understanding

---

## ⚙️ 7. How Word2Vec Training Actually Works

---

### 📌 Sliding Window Concept

The model processes text using a sliding window.

---

### 🧠 Example Sentence

```text
"The cat sat on the mat"
```

---

### Window size = 3

We take chunks:

```text
(cat, sat) → on
(sat, on) → the
(on, the) → mat
```

---

### 💡 Explanation

* Input = surrounding words
* Output = target word

---

### 🔁 This repeats across entire dataset

* Wikipedia
* Google News
* Internet data

---

## 🧠 8. What is “Epoch”?

Epoch = one full pass through data

---

### 💡 During training

* Data is passed multiple times
* Each time → weights improve

---

## ⚖️ 9. Final Output After Training

After:

* millions of iterations
* billions of samples

We get:

> One vector per word

---

## 📐 10. What Does Vector Size Mean?

Example:

* 3-dimensional vector → [x, y, z]
* 300-dimensional vector → 300 numbers

---

### 💡 Important

Vector size is:

> A design choice (hyperparameter)

---

### Example:

* 3 → simple understanding
* 100 → better
* 300 → richer meaning

---

## ❗ Clarification

Vector size ≠ number of meanings

---

## 🧠 11. Why Not Use Single Number?

You might think:

> Why not assign just one number per word?

---

### ❌ Problem

One number cannot capture:

* multiple meanings
* relationships
* context patterns

---

### 💥 Solution

Use multiple dimensions → vector

---

## 🔁 12. Important Insight from Discussion

Even if:

* a word appears in different positions
* or different sentences

👉 Its embedding remains SAME

---

### 💡 Key Statement

> Word2Vec is NOT position-aware
> Word2Vec is NOT context-aware

---

## 🧠 13. What Word2Vec CAN Do Well

* Capture word similarity
* Learn relationships
* Understand usage patterns

---

### Example:

cat ≈ dog
king → queen
man → woman

---

## ⚠️ 14. What Word2Vec CANNOT Do

* Understand sentence meaning
* Handle ambiguity (bank, interest)
* Capture dynamic context

---

## 🔗 15. Practical Implementation (VERY IMPORTANT)

---

### Two approaches:

---

### 🔹 Option 1: Train Your Own Model

Using your own dataset:

```python
from gensim.models import Word2Vec

model = Word2Vec(sentences, vector_size=100)
```

---

### 🔹 Option 2: Use Pretrained Model

Example:

* Google News Word2Vec
* ~300-dimensional vectors
* trained on billions of words

---

### 💡 Insight

Pretrained models:

* more accurate
* already trained on huge data

---

## ⚠️ 16. Practical Constraints

* Model size ≈ 1.5GB–2GB
* Requires good RAM
* Needs good internet for download

---

## 🧭 17. Final Mental Model

```text
Step 1: Take large text data
Step 2: Slide window across words
Step 3: Predict target word
Step 4: Adjust weights (backpropagation)
Step 5: Repeat millions of times
Step 6: Assign one vector per word
```

---

## 🏁 18. Summary

* Word2Vec converts words into meaningful vectors
* Training uses context prediction
* Sliding window generates training data
* Each word gets ONE vector
* Same word → same vector everywhere
* Cannot capture sentence-level meaning
* This limitation leads to Transformers

---

## 💡 Final Insight

Word2Vec is a major breakthrough because it introduced **meaningful word representations**.

However:

> It captures meaning at the word level, not at the sentence level.

This limitation is what led to the next evolution in AI — Transformers.

---
# 📘 N-Grams Explained — Concept, Examples & Relation to Word2Vec

---

## 🧠 1. What is an N-gram?

> An **n-gram** is a sequence of **n consecutive words** from a sentence.

It is one of the earliest techniques used in NLP to capture **local context**.

---

## 📌 2. Basic Types of N-grams

Consider the sentence:

```text
"I love machine learning"
```

---

### 🔹 Unigram (n = 1)

Single words:

```text
I, love, machine, learning
```

---

### 🔹 Bigram (n = 2)

Two-word sequences:

```text
I love
love machine
machine learning
```

---

### 🔹 Trigram (n = 3)

Three-word sequences:

```text
I love machine
love machine learning
```

---

## 💡 3. Why Do We Need N-grams?

Single words often lose meaning.

Example:

```text
"bank"
```

We don’t know:

* river bank
* bank account

---

### ✅ Using N-grams:

```text
"river bank"
"bank account"
```

👉 Now the meaning becomes clearer.

---

### 💥 Key Insight

> N-grams help capture **local context (nearby words)**

---

## ⚙️ 4. How N-grams Work

N-grams use a **sliding window** approach.

---

### Example:

Sentence:

```text
"The cat sat on the mat"
```

---

### Bigrams:

```text
The cat
cat sat
sat on
on the
the mat
```

---

👉 The window slides one word at a time.

---

## 🧠 5. Where N-grams Are Used

---

### 🔹 1. Search Engines

Query:

```text
"best coffee shop"
```

System uses:

* "best coffee"
* "coffee shop"

---

### 🔹 2. Text Prediction (Old Models)

Example:

```text
"I love machine → ?"
```

👉 Based on bigrams/trigrams:
→ learning

---

### 🔹 3. TF-IDF

Instead of just:

```text
machine, learning
```

We use:

```text
machine learning
```

👉 Improves relevance

---

### 🔹 4. Spam Detection

Patterns like:

```text
"win money now"
"free offer today"
```

---

## 🔗 6. Relation to Word2Vec

---

### 🧠 N-grams vs Word2Vec

| Concept  | What it captures    |
| -------- | ------------------- |
| N-grams  | Local word patterns |
| Word2Vec | Semantic meaning    |

---

### 💡 Key Difference

#### 🔹 N-grams:

* Look at **exact word sequences**
* Example:

```text
"machine learning"
```

---

#### 🔹 Word2Vec:

* Learns meaning from context
* Example:

```text
machine ≈ computer
learning ≈ training
```

---

### 💥 Important Insight

> N-grams capture **surface-level relationships**
> Word2Vec captures **deeper semantic relationships**

---

## 🔗 7. How N-grams Connect to Word2Vec

Word2Vec also uses a similar idea:

👉 It looks at **neighboring words**

But instead of storing phrases like n-grams:

👉 It **learns patterns through training**

---

### Example

Sentence:

```text
"The cat sat on the mat"
```

---

#### N-grams:

```text
cat sat
sat on
```

---

#### Word2Vec learns:

* cat appears near sat
* sat appears near on

👉 Learns relationships, not just sequences

---

## ⚠️ 8. Limitations of N-grams

---

### ❗ 1. Data Explosion

More combinations → more storage

---

### ❗ 2. No Deep Meaning

* "good movie"
* "great movie"

👉 treated as different

---

### ❗ 3. Fixed Context Window

Only looks at nearby words
👉 misses long-range relationships

---

## 🚀 9. Why Word2Vec Replaced N-grams

N-grams:

* store patterns

Word2Vec:

* learns patterns

---

### 💥 Key Upgrade

```text
N-grams → static patterns
Word2Vec → learned meaning
```

---

## 🧭 10. Final Mental Model

```text
Text
 ↓
Tokenization
 ↓
N-grams (local context)
 ↓
TF-IDF (importance)
 ↓
Word2Vec (semantic meaning)
 ↓
Transformers (full context understanding)
```

---

## 🏁 11. Summary

* N-grams are sequences of consecutive words
* They capture local context using sliding windows
* Useful in search, TF-IDF, and simple NLP tasks
* Limited because they don’t understand meaning
* Word2Vec improves this by learning semantic relationships

---

## 💡 Final Insight

> N-grams are the first step toward understanding context
> Word2Vec is the next step toward understanding meaning

---
# 📘 Advanced Notes — Embeddings, Similarity, Limitations & Sentence Vectors

---

## 🧠 1. Proof That Embeddings Carry Meaning

One of the strongest validations of embeddings is the ability to perform **mathematical operations on words**.

---

### 💡 Example

```text
king - man + woman ≈ queen
```

---

### 🧠 What this shows

* Words are converted into vectors (e.g., 300 dimensions)
* These vectors are not random
* They encode **semantic meaning**

---

### 💥 Insight

> Embeddings are not just numbers — they represent relationships between words 

---

## ⚠️ 2. Core Limitation — One Word, One Vector

Even though embeddings are powerful:

> Each word has only ONE vector representation

---

### 🧠 Example: "bank"

* river bank
* bank account

👉 Same word → same vector

---

### 💥 Problem

The model cannot distinguish meaning based on sentence.

---

### 💡 Insight

> Word2Vec embeddings are **context-independent**

---

## 🔍 3. Exploring Similar Words

Using pretrained models, we can find:

```python
most_similar("bank")
```

---

### 🧠 Observation

* bank → banking, banker, lender, depositor

👉 Mostly financial meaning

---

### 💥 Why?

Because:

* training data had more financial context

---

## ⚠️ 4. Out-of-Vocabulary (OOV) Problem

If a word is not present in training data:

```text
ChatGPT → not found
```

---

### 💥 Insight

> Model only knows what it has seen during training

---

## 🧠 5. Stop Words in Embeddings

Earlier (TF-IDF stage):

* stop words were removed

Now (embeddings stage):

> Stop words are NOT removed

---

### 💡 Why?

Because:

* "not good" ≠ "good"
* stop words affect **meaning and context**

---

## 🔁 6. Stemming / Lemmatization vs Embeddings

Earlier:

* "run", "running" → same root

Now:

> Each word has its own vector

---

### 💥 Insight

* run → separate vector
* running → separate vector

👉 Meaning is learned, not reduced

---

## 🧠 7. How Sentence Embeddings Are Created

Word2Vec gives:

```text
Word → Vector
```

---

### 🎯 Problem

How do we represent a full sentence?

---

### 💡 Solution (Simple Approach)

Average all word vectors

---

### 🧮 Example

```text
the → [1,2,3]
cat → [4,5,6]
sat → [7,8,9]
```

---

### Step:

```text
Sentence vector = (the + cat + sat) / 3
```

---

### 💥 Insight

> Sentence meaning = average of word meanings

---

## ⚠️ 8. Limitation of Sentence Averaging

* Loses word order
* Loses structure
* Weak understanding of grammar

---

## 📐 9. Vector Dimensions (Important Concept)

Different models use different vector sizes:

---

### Examples:

* Word2Vec (Google News) → 300 dimensions
* OpenAI embeddings → 1536 / 3072
* Gemini embeddings → 3072

---

### 💡 Insight

> Vector size is a design choice (hyperparameter)

---

### ❗ Important

Vector size ≠ number of meanings

---

## 🔗 10. What Do These Numbers Represent?

Each dimension captures some aspect of meaning:

* context
* usage
* relationships

---

### 💥 Insight

> Meaning is distributed across multiple dimensions

---

## 🧠 11. What is Embedding (Final Definition)

> Embedding is the process of converting a word into a vector that captures its meaning across multiple dimensions.

---

## ⚠️ 12. Key Limitations Recap

---

### ❗ 1. Context Problem

Same word → same vector

---

### ❗ 2. OOV Problem

Unknown words → no vector

---

### ❗ 3. Sentence Weakness

Averaging loses structure

---

## 🚀 13. Why We Move Beyond Word2Vec

Because:

* meaning depends on context
* sentence structure matters

---

### 💥 This leads to:

* Contextual embeddings
* Transformers
* Attention mechanisms

---

## 🧭 14. Final Mental Model

```text
Word → Vector (Word2Vec)
Sentence → Average of vectors
Meaning → Encoded in numbers
Limitation → No context awareness
Solution → Transformers
```

---

## 🏁 15. Summary

* Embeddings capture meaning numerically
* Vector math proves semantic relationships
* Each word has a fixed vector
* Cannot handle multiple meanings
* Sentence embeddings can be approximated using averaging
* Leads to next evolution → Transformers

---

## 💡 Final Insight

> Word2Vec was a breakthrough because it introduced meaningful word representations, but its inability to handle context led to the rise of modern NLP architectures.

---
# 📘 Advanced Notes — Embedding Selection, Preprocessing Trade-offs & Real-World Design Decisions

---

## 🧠 1. Big Shift — From Learning Concepts to Making Decisions

At this stage, the focus moves from:

> “What is embedding?”

to

> “Which embedding should I use and why?”

---

### 💡 Key Insight

> Every AI system requires choosing the right embedding model based on the use case 

---

## 🔗 2. Multiple Embedding Models Exist

Different organizations provide their own embeddings:

* Google (Word2Vec, Gemini embeddings)
* OpenAI (text-embedding models)
* Meta (FastText)

---

### 💡 Important Understanding

> There is no single “best” embedding model

---

### Instead:

Selection depends on:

* use case
* domain
* data type
* performance needs

---

## ⚙️ 3. Choosing the Right Embedding Model

---

### 🧠 Key Factors

#### 🔹 1. Domain-Specific Data

Example:

* Healthcare chatbot → use healthcare-trained embeddings
* Legal documents → use legal embeddings

---

#### 🔹 2. Type of Data

* Generic text → general embeddings
* Company-specific data → custom-trained embeddings

---

### 💥 Insight

> If your data is very specific, pretrained models may not understand it properly

---

## 🧠 4. When Should You Train Your Own Model?

---

### 📌 Scenario

If your data contains:

* internal terminology
* company-specific keywords
* domain-specific abbreviations

---

### 💡 Example

Company uses:

```text
DMD → Demand
```

---

### ❗ Problem

Pretrained model does NOT understand this mapping

---

### 💥 Solution

> Train your own embedding model or provide context explicitly

---

## 🔗 5. Embeddings + LLM + Schema (Important Concept)

---

### 🧠 Problem

User asks:

```text
"What is the demand?"
```

Database column:

```text
DMD
```

---

### ❗ Issue

Embedding cannot match:

* "demand" ≠ "DMD"

---

### 💡 Solution

Provide:

* metadata
* schema
* column definitions

---

### 💥 Insight

> LLM needs context (schema/metadata) to map natural language to structured data

---

## ⚠️ 6. Preprocessing Debate — Stemming & Lemmatization

This was a critical discussion.

---

### 🔹 Old Approach (TF-IDF)

* remove stop words
* apply stemming
* reduce vocabulary

---

### 🔹 New Approach (Embeddings)

> Do NOT apply stemming or lemmatization by default

---

### 💥 Why?

Because:

* embeddings rely on full word meaning
* removing parts may distort meaning

---

## ⚖️ 7. Trade-off — Accuracy vs Speed

---

### 🧠 Scenario

Large dataset (e.g., resumes, e-commerce data)

---

### Option 1: No preprocessing

* ✅ better accuracy
* ❌ slower search

---

### Option 2: Apply stemming/lemmatization

* ✅ faster search
* ❌ possible loss of meaning

---

### 💡 Key Decision

> Depends on use case

---

### 🔥 Real Insight

> Faster wrong answer is worse than slower correct answer

---

## 🧠 8. Chunking & Vector Search

When building applications:

* data is split into chunks
* each chunk → converted to vector
* stored in vector database

---

### 💡 Question Raised

Can preprocessing reduce chunks?

---

### Answer

Yes — but:

> It may reduce context quality

---

## ⚠️ 9. Important Risk

If you:

* remove words
* alter structure

👉 embedding quality reduces

---

## 🧠 10. Out-of-Vocabulary (OOV) Revisited

---

### 📌 Problem

Word not present in training:

```text
ChatGPT → not found
```

---

### 💡 Reason

Model trained on old dataset

---

### 💥 Insight

> Models only know what they were trained on

---

## 🚀 11. Evolution Beyond Word2Vec — FastText

---

### 📌 Problem with Word2Vec

* Cannot handle unknown words
* Cannot handle sub-word structure

---

### 💡 Solution: FastText (2017)

Introduced by Meta (Facebook)

---

### 🔹 Key Idea

Instead of learning:

* word → vector

It learns:

> sub-words → vector

---

### 🧠 Example

Word: "running"

FastText breaks into:

```text
run, runn, unning, etc.
```

---

### 💥 Advantage

* Handles unseen words
* Better generalization

---

## 🔗 12. Key Difference — Word2Vec vs FastText

| Feature        | Word2Vec   | FastText  |
| -------------- | ---------- | --------- |
| Input          | Whole word | Sub-words |
| OOV handling   | ❌ No       | ✅ Yes     |
| Generalization | Limited    | Better    |

---

## 🧭 13. Real-World Thinking (Most Important Part)

---

### 💡 When building applications:

You must decide:

* Accuracy vs Speed
* Generic vs Domain-specific
* Pretrained vs Custom

---

### 💥 There is no fixed rule

> Engineering decisions depend on constraints

---

## 🏁 14. Final Mental Model

```text
Text
 ↓
Preprocessing (optional)
 ↓
Embedding (model choice)
 ↓
Vector DB
 ↓
Search / Retrieval
 ↓
LLM (with context)
```

---

## 💡 Final Insight

> AI systems are not just about models — they are about making the right design decisions.

---

## 🔥 Key Takeaways

* Embedding model choice is critical
* Preprocessing is not always beneficial
* Context (schema/metadata) is essential
* Word2Vec has limitations → FastText improves it
* Real-world AI = trade-offs, not fixed rules

---
