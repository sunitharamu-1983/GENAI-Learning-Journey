# EMBEDDINGS

---

## What are embeddings? 
Computers do not understand words and can only fathom numbers. For the computer to begin making sense of what you say, everything must be converted from words to numbers and that conversion is called an embedding.

## What is a vector? 
Every word can have a number totally unrelated to each other. But if the word to number conversion is good, in short, if the embedding is good - then the words that are similar in meaning are close to each other in the number space. This number space is called a vector space and can also be called coordinates in an N-dimensional space.

**Note:** *Each word's embedding is essentially its coordinates in this space — and words with similar meanings end up with similar coordinates after training.*

Embeddings have evolved significantly over time — each generation fixing the limitations of the previous one. The key milestones are as follows. 

**Types of Important Embeddings**

1. Bag of Words(BOW)
2. Term Frequency - Inverse Document Frequency (TF - IDF)
3. Word2Vec
4. GLOVE
5. FastText

---

## Bag of Words (BOW) Embedding

```
Example: Let's say you have 3 sentences.

S1 - "I love India" 
S2 - "I love Mango" 
S3 - "Mango is a seasonal fruit"
```

- **Step 1:** BOW builds a vocabulary of unique words: I, love, India, Mango, is, a, seasonal, fruit
- **Step 2:** Builds a vector for each sentence, by counting how many times each word from the vocabulary appears in the sentence.

*Thus you get the bag of words as an embedding, raw data. No meaning. Love is there in S1 and S2. But what meaning or context can be inferred? Practically - None. It helped you classify the document, by representing the document/sentences as vectors.* 

## Problems in BOW

1. No meaning can be derived. I can love mango and mango is a seasonal fruit and that need not imply that I love any seasonal fruit.
2. Order doesn't matter here.
3. If the sentence is small, the vector is manageable. Imagine a vocabulary with 50,000 words. Multiple vectors are built with majority 0s. This is called a **sparse vector** and is computationally expensive and inefficient.
4. Every word is treated equally and from our example, we understand that the common **stop words** like **"is", "a"** all get the same weightage as **"Mango"**. 

**Summary:** *BOW is an embedding with just numbers obtained by counting, its a good start - but it's blind to meaning, order, importance.*

---
