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

### Problems in BOW

1. No meaning can be derived. I can love mango and mango is a seasonal fruit and that need not imply that I love any seasonal fruit.
2. Order doesn't matter here.
3. If the sentence is small, the vector is manageable. Imagine a vocabulary with 50,000 words. Multiple vectors are built with majority 0s. This is called a **sparse vector** and is computationally expensive and inefficient.
4. Every word is treated equally and from our example, we understand that the common **stop words** like **"is", "a"** all get the same weightage as **"Mango"**. 

**Summary:** *BOW is an embedding with just numbers obtained by counting, its a good start - but it's blind to meaning, order, importance.*

---

## Term Frequency - Inverse Document Frequency (TF-IDF) Embedding

Term Frequency (TF) and Inverse Document Frequency (IDF) helps to overcome problem 4 of BOW - **IMPORTANCE**. That is: Words which appear across multiple sentences in a document will not be unique or will not be given a higher importance as its not rare. Words which has an overall higher TF-IDF score, will be termed important & rare in the embedding. 

```
Example: Let's say you have 3 sentences.

S1 - "I love India" 
S2 - "I love Mango" 
S3 - "Mango is a seasonal fruit"
```
### Part 1 — TF (Term Frequency)
This is essentially BOW — just counting how many times a word appears in a document. But instead of raw count, we normalise it:
```
The formula is: TF = (Number of times word appears in document) / (Total words in document)
```
So, 
S2 = "I love Mango" — 3 words total
TF of "Mango" in S2 = 1/3 = 0.33 (Simple) 

*But **TF alone** still has BOW's Problem 4 — "is" and "a" would still score high if they appear often.*

### Part 2 — IDF (Inverse Document Frequency)
This is where TF-IDF gets smart. **The idea is:** If a word appears in every document — it's probably not important. If a word appears in very few documents — it's probably important, very important or even rare. 
```
The formula is: IDF = log(Total number of documents / Number of documents containing the word)
```
So, 
```
Word                  How many times?                        IDF
-----------------------------------------------------------------------
I                            2/3                       log(3/2) = 0.17
love                         2/3                       log(3/2) = 0.17
Mango                        2/3                       log(3/2) = 0.17
India                        1/3                       log(3/1) = 0.48
is                           1/3                       log(3/1) = 0.48
a                            1/3                       log(3/1) = 0.48
seasonal                     1/3                       log(3/1) = 0.48
fruit                        1/3                       log(3/1) = 0.48
```
From this, not just "seasonal" & "fruit" - "is" and "a" in this example corpus seems to be important words. This is with respect to just IDF for this corpus. 

### Example Calculation - TFxIDF

Now - Lets do a TF x IDF, the aggregated score for the example corpus

```
Step 1 — Calculate TF for each word in each sentence
TF = Word count in sentence / Total words in sentence

Word                    S1                    S2                    S3                                      
------------------------------------------------------------------------------
I                       1/3 = 0.33            1/3 = 0.33            0
love                    1/3 = 0.33            1/3 = 0.33            0
India                   1/3 = 0.33            0                     0
Mango                   0                     1/3 = 0.33            1/5 = 0.20
is                      0                     0                     1/5 = 0.20
a                       0                     0                     1/5 = 0.20
seasonal                0                     0                     1/5 = 0.20
fruit                   0                     0                     1/5 = 0.20
```

```
Step 2 — Calculate IDF for each word
IDF = log(Total documents / Documents containing the word)

Word                    Appears in how many sentences                  IDF = log(3/n)                                    
--------------------------------------------------------------------------------------
I                       2 (S1, S2)                                     log(3/2) = 0.18
love                    2 (S1, S2)                                     log(3/2) = 0.18
India                   1 (S1)                                         log(3/1) = 0.48
Mango                   2 (S2, S3)                                     log(3/2) = 0.18
is                      1 (S3)                                         log(3/1) = 0.48
a                       1 (S3)                                         log(3/1) = 0.48
seasonal                1 (S3)                                         log(3/1) = 0.48
fruit                   1 (S3)                                         log(3/1) = 0.48
```

```
Step 3: TF x IDF = Aggregated Scores

S1 = "I love India"
Word                    TF              IDF              TFxIDF
------------------------------------------------------------------
I                       0.33            0.18             0.0594
love                    0.33            0.18             0.0594
India                   0.33            0.48             0.158

"India" scores the highest - Appears only once


S2 = "I love Mango"
Word                    TF              IDF              TFxIDF
------------------------------------------------------------------
I                       0.33            0.18             0.0594
love                    0.33            0.18             0.0594
Mango                   0.33            0.18             0.0594

No unique words

S3 = "Mango is a seasonal fruit"
Word                    TF              IDF              TFxIDF
------------------------------------------------------------------
Mango                   0.20            0.18             0.036
is                      0.20            0.48             0.096
a                       0.20            0.48             0.096
seasonal                0.20            0.48             0.096
fruit                   0.20            0.48             0.096

"Seasonal" & "Fruit" scores the highest - Appears only once
```
***Insight: TF-IDF has mathematically confirmed that "India" is the soul of S1, and "seasonal" and "fruit" are the soul of S3 — without anyone telling it so.***

So, when this pattern is applied to a bigger corpus lets say with 50,000 tokens - the TF-IDF score will give an embedding with high scores for the important items. 

### Problems in TF-IDF

1. No meaning can be derived. I can love mango and mango is a seasonal fruit and that need not imply that I love any seasonal fruit.
2. Order doesn't matter here.
3. If the sentence is small, the vector is manageable. Imagine a vocabulary with 50,000 words. Multiple vectors are built with majority 0s. This is called a **sparse vector** and is computationally expensive and inefficient.

---

## Word2Vec Embedding

Word2Vec was invented in 2013 by a team at Google to fix the drawbacks from BOW & TF-IDF, precisely to give words a sense of relationship and meaning.

```
Example: Mango is a seasonal fruit
```

The word "Mango" appears near "seasonal" and "fruit", so over millions of sentences, Word2Vec learns that Mango belongs in the same neighbourhood as "apple", "banana", "orange" — because they ALL appear near words like "seasonal", "fruit", "eat" and so on. It was not coded, it figured it out from the context alone.

### Approaches to Word2Vec

There are two approaches to Word2Vec.
1. Continous Bag of Words (CBOW)
2. SkipGram

Before we get into the approach details, let us understand if BOW and CBOW are the same or different. 

***Summary: They are two different concepts. BOW is standalone embedding technique and the CBOW is one among the Word2Vec approaches.***

Category | BOW | CBOW |
---------|-----|------|
Full Form|Bag of Words|Continous Bag of Words|
Standalone Embedding|✅ Yes|❌ No|
Purpose|Counts word occurrences in a document|Predicts a missing word from surrounding context|
Output|A vector of counts|A dense, meaningful embedding|
Understands Meaning|❌ No|✅ Yes|

S1 — "I love India"
S2 — "I love Mango"
S3 — "Mango is a seasonal fruit"


### How CBOW works — Step by Step

CBOW uses a context window, a fixed number of words on either side of the target word. Let's use a window of 1 (one word on each side) for simplicity.

```
Example: Let's say you have 3 sentences.

S1 - "I love India" 
S2 - "I love Mango" 
S3 - "Mango is a seasonal fruit"
```

#### Working through S3 — "Mango is a seasonal fruit"
CBOW slides through the sentence and creates training pairs like this:

Context Words (Input)|Target Word (Predict)|
---------------------|---------------------|
Mango, a|is|
is, seasonal|a|
a, fruit|seasonal|
seasonal, (end)|fruit

For each pair, the model:
1. Takes the context words — "Mango" and "a"
2. Averages their vectors together into one combined vector
3. Asks — "given this combined meaning, what word sits in the middle?"
4. Makes a prediction across the entire vocabulary
5. Checks if it got "is" right
6. Back propagates and nudges the vectors

#### Working through S2 — "I love Mango"

Context Words (Input)|Target Word (Predict)|
---------------------|---------------------|
I, Mango|love|
love, (end)|Mango|

"I" and "Mango" are the context and "love" is what the model has to predict. Over millions of similar sentences, the model learns that "love" and "like" and "enjoy" all appear in similar contexts — so they end up as neighbours in vector space.

#### Working through S1 — "I love India"

Context Words (Input)|Target Word (Predict)|
---------------------|---------------------|
I, India|love|
love, (end)|India

