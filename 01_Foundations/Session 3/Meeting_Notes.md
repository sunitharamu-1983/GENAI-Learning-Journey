# 📘 Session Notes — NLP & Text to Numbers

---

## 🎯 1. Course Learning Strategy

### 📌 How to approach the course

* Go through **technical content shared by instructor**
* Complete **assignments**
* Work on **hands-on projects**
* Modify and extend given examples

---

### 💡 Key Expectation

> Understanding is not enough → You should be able to **explain concepts clearly**

---

### 🧠 Reality Check

* Concepts may require **multiple revisions (2–10 times)**
* Initial difficulty is expected

---

## 🔗 2. Evolution of AI

### 📊 Flow

Statistics → Probability → Machine Learning → Deep Learning → Generative AI

---

### 🧠 Breakdown

#### 🔹 Statistics

* Describes past data
* Example: average attendance

#### 🔹 Probability

* Predicts future outcomes
* Example: chance of success

#### 🔹 Machine Learning

* Learns patterns from data
* Uses algorithms (classification, regression)

#### 🔹 Deep Learning

* Mimics human brain (neurons)
* Handles complex patterns

#### 🔹 Generative AI

* Generates new content:

  * Text
  * Images
  * Audio

---

### 💥 Core Insight

> Every stage of AI ultimately works on **numbers**

---

## 🔢 3. Core Concept — Everything Becomes Numbers

### 💡 Key Idea

Even if input is:

* Text
* Image
* Audio

👉 It is converted into **numbers** before processing

---

### 🧠 Why?

> Algorithms understand only numbers

---

### 🔗 Flow

Text / Image / Audio
↓
Preprocessing
↓
Convert to Numbers
↓
Algorithm

---

### ⚠️ Important Note

* Conversion to numbers = **techniques (not algorithms)**
* Algorithms operate **after conversion**

---

## 🧾 4. Role of NLP

### 💡 What NLP does

* Processes human language (text)

---

### 🎯 Problem

* Machines cannot understand text directly
* Machines understand only numbers

---

### 💥 Solution

> Convert TEXT → NUMBERS

---

## 🔧 5. One Hot Encoding

### 💡 What it is

A method to convert text into a **binary matrix (0s and 1s)**

---

### 🧠 Example

Text:
"movie is good"

---

### Step 1: Create vocabulary (corpus)

movie, is, good, bad, worst

---

### Step 2: Convert into representation

| movie | is | good | bad |
| ----- | -- | ---- | --- |
| 1     | 1  | 1    | 0   |

---

### 📊 Interpretation

* 1 → word present
* 0 → word absent

---

### 📌 Use Case

* Classification tasks (e.g., sentiment analysis)

---

## ⚠️ 6. Problems with One Hot Encoding

### ❗ High Dimensionality

* Large vocabulary → too many columns

### ❗ Sparsity

* Mostly zeros → inefficient

### ❗ No Semantic Meaning

* "good" and "excellent" treated as unrelated

### ❗ Repetition Issue

* Does not capture importance of word frequency

---

## 📚 7. Important Term — Corpus

> Corpus = collection of all documents/text data

---

## 🔗 8. Full System View

User Input (Text)
↓
NLP Processing
↓
Convert to Numbers (One-hot / TF-IDF / Embeddings)
↓
Model (ML / DL / LLM)
↓
Output

---

## 🔥 9. Evolution of Text Processing

### Old Approach

Text → One Hot Encoding → ML Model

---

### Modern Approach

Text → Embeddings → Vector DB → LLM → Output

---

## 💡 10. Key Insights

* All AI systems operate on numbers
* Text must be converted into numbers before processing
* One-hot encoding is a basic technique with limitations
* NLP bridges human language and machine understanding
* Modern AI uses embeddings instead of one-hot encoding for better semantic understanding

---

## 🧭 Summary

NLP enables machines to process text by converting it into numerical form.
This numerical representation is then used by machine learning and AI models to generate outputs.

The evolution from one-hot encoding → TF-IDF → embeddings reflects increasing ability to capture meaning, not just words.

---
# 📘 Deep Learning Basics for NLP (Weights, Layers, Backpropagation)

---

## 🧠 1. Big Picture First

Before going into terms, understand this:

A neural network is simply a system that:

* takes input (numbers)
* processes it through layers
* produces an output (prediction)

In NLP (like Word2Vec), the goal is:

> Given some words → predict another word

---

## ⚙️ 2. What are Layers?

A neural network has **3 main types of layers**:

### 🔹 Input Layer

* Where data enters the system
* Example: words converted into numbers (vectors)

---

### 🔹 Hidden Layer

* Where **learning happens**
* This is where patterns are formed
* In Word2Vec, this layer becomes the **embedding (meaning representation)**

---

### 🔹 Output Layer

* Final prediction
* Example: predicted word

---

### 💡 Simple Flow

Input → Hidden Layer → Output

---

## 🧠 3. What are Weights?

### 💡 Definition

Weights are **numbers that control how important each input is**

---

### 🧠 Think of it like this:

You are making a decision:

```text
Output = (Input1 × Weight1) + (Input2 × Weight2)
```

---

### 🔹 Example (Real-life analogy)

Predict gender from:

* height
* weight

```text
Output = (height × 0.6) + (weight × 0.4)
```

👉 Here:

* 0.6 and 0.4 = weights
* They define importance

---

### 💥 In Neural Networks

* Every connection between neurons has a weight
* These weights are **learned automatically**

---

## 🔁 4. What is Backpropagation?

### 💡 Definition

Backpropagation is the process of:

> **correcting weights when the prediction is wrong**

---

### 🧠 Step-by-step intuition

1. Model makes a prediction
2. Compare with actual answer
3. Calculate error
4. Go back and adjust weights
5. Repeat many times

---

### 🔄 Example

Prediction: "dog"
Actual: "cat"

👉 Error exists

So system:

* adjusts weights
* tries again

---

### 💥 Key Idea

> The model improves by learning from mistakes

---

## ⚙️ 5. How Layers Actually Work Together

Let’s simplify what your instructor showed.

---

### Step 1: Input comes in

Example:

```text
"cat" and "sat"
```

Converted into vectors (numbers)

---

### Step 2: Pass through hidden layer

* Inputs are multiplied with weights
* Combined together
* Passed forward

---

### Step 3: Output layer predicts

Example:

```text
Predicted word = "on"
```

---

### Step 4: Compare with actual

Actual:

```text
"on"
```

If correct → good
If wrong → adjust weights

---

### Step 5: Backpropagation

* Error is sent backward
* Weights are updated
* Model improves

---

## 🧠 6. Why Hidden Layer is Important

The hidden layer:

* compresses information
* learns patterns
* captures relationships

---

### 💥 In Word2Vec

Hidden layer = **word embedding**

👉 This is where meaning is stored

---

## 🔗 7. Connecting to Embeddings

Full flow:

```text
Words → Input Layer → Hidden Layer → Output Layer
           ↓              ↓
      Numbers         Meaning (Embeddings)
```

---

## 💡 8. Key Insights

* Weights determine how inputs influence outputs
* Backpropagation adjusts weights using error
* Hidden layers learn patterns and meaning
* More layers → deeper learning
* Embeddings come from hidden layers

---

## 🧭 9. Simple Mental Model

Think of it like learning:

* First attempt → wrong
* Adjust thinking
* Try again
* Improve over time

👉 That is exactly what the model does

---

## 🏁 10. Final Summary

A neural network learns by:

* taking inputs
* applying weights
* predicting outputs
* correcting itself using backpropagation

Over time, it becomes better at understanding patterns —
which in NLP results in meaningful word representations (embeddings).

---
