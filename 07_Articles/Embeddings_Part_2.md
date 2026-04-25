# Embeddings - Part 2 - GloVe & FastText

## GloVe — Global Vectors for Word Representation

**GloVe was developed at Stanford in 2014 — one year after Word2Vec.**

### Why GloVe was needed
Word2Vec was a giant leap — but it had one limitation:

Word2Vec learns from a local context window — it only looks at the immediate neighbours of a word, a few words at a time. GloVe asked a smarter question:
*"Instead of sliding a window through the corpus — what if we counted how often every word appears with every other word across the entire corpus at once?"*

This is called Global Co-occurrence — and that is exactly where the name comes from: GloVe = Global Vectors

### Step 1 — Building the Co-occurrence Matrix

```
Example:
S1 — "I love India"
S2 — "I love Mango"
S3 — "Mango is a seasonal fruit"
```

GloVe first builds a Co-occurrence Matrix — a table that counts how many times every word appears near every other word across ALL sentences simultaneously.
With a window of 1:

||I|love|India|Mango|is|a|seasonal|fruit|
-|-|----|-----|-----|--|-|--------|-----|
I|0|2|0|0|0|0|0|0|
love|2|0|1|1|0|0|0|0|
India|0|1|0|0|0|0|0|0|
Mango|0|1|0|0|1|0|0|0|
is|0|0|0|1|0|1|0|0|
a|0|0|0|0|1|0|1|0|
seasonal|0|0|0|0|0|1|0|1|
fruit|0|0|0|0|0|0|1|0|

Reading the matrix:
```
"I" and "love" appear next to each other 2 times — once in S1, once in S2
"love" and "India" appear next to each other 1 time — in S1
"love" and "Mango" appear next to each other 1 time — in S2
"Mango" and "is" appear next to each other 1 time — in S3
"I" and "Mango" — 0 times — they never appear as immediate neighbours
```

### Step 2 — What GloVe does with this matrix
This is where GloVe gets clever. It looks at the ratios of co-occurrence probabilities — not just raw counts.

```
For example:
"Mango" co-occurs with "fruit" ✅
"Mango" co-occurs with "seasonal" ✅
"Mango" co-occurs with "India" ❌ — never
```

So the ratio of P(fruit | Mango) to P(India | Mango) is very high — meaning "fruit" is far more related to "Mango" than "India" is. GloVe trains word vectors so that their dot product equals the log of their co-occurrence count. This ensures:

***Words that appear together often end up close in vector space. Words that never appear together end up far apart.***

### The key difference from Word2Vec
||Word2Vec|GloVe|
-|--------|-----|
Looks at|Local context window — a few words at a time|Global co-occurrence — entire corpus at once|
Learning method|Predicts words (CBOW or Skip-Gram)|Factorizes the co-occurrence matrix|
Captures|Local relationships|Global statistical patterns|
Speed|Slower on large corpus|Faster — matrix built once, then trained|
Example strength|"Mango" near "fruit" in one sentence"|Mango" near "fruit" across ALL sentences simultaneously|

### What GloVe still can't do:

- No meaning between words --> **Fixed** — rich relationships
- Sparse vectors --> **Fixed** — dense vectors
- Local context only --> **Fixed** — global co-occurrence
- One word, one meaning (Polysemy) --> **Still not fixed** — "Apple" the fruit and "Apple" the company still get one vector
- Unknown words (Out of Vocabulary) --> **Not fixed** — if a word wasn't in training data, GloVe has no vector for it

***That last problem — Out of Vocabulary words — is exactly what FastText was built to fix. 🎯***

##### One line to remember : Word2Vec looks at the neighbourhood. GloVe looks at the entire city — all at once.

---

## Layman Analogy:

*Imagine you want to understand which team members work closely together. Word2Vec would shadow each person individually and observe who they talk to during the day. GloVe would pull the entire email and chat history of the organisation at once and count — across all time — who communicated with whom and how often. GloVe sees the full picture, not just today's snapshot.*

---

## FastText — Sub-word Embeddings

FastText was developed by **Facebook AI Research (FAIR) in 2016.**

### Why FastText was needed

*Both Word2Vec and GloVe had one shared blind spot:If a word was never seen during training — they had absolutely no vector for it. This is called an Out of Vocabulary (OOV) problem.*

### The Core Idea — Breaking words into pieces

FastText learns vectors for **sub-words** — small character chunks called **character n-grams.**

Using *"Mango"* with n=3 (trigrams):

| Sub-word chunks |
|---|
| \<Ma |
| Man |
| ang |
| ngo |
| go\> |
| \<Mango\> |

The < and > symbols mark the beginning and end of a word — so FastText knows it's dealing with a complete word boundary, not a fragment from inside another word.
The final vector for "Mango" = sum of all its sub-word vectors. The final vector for *"Mango"* = **sum of all its sub-word vectors.**

### How this solves OOV

Now imagine a word FastText has **never seen** — *"Mangoes"*

FastText breaks it down:

| Sub-word chunks |
|---|
| \<Ma |
| Man |
| ang |
| ngo |
| oes |
| go\> |

It recognises "<Ma", "Man", "ang", "ngo" — it has seen these before in "Mango"! So it constructs a reasonable vector for "Mangoes" from familiar pieces — even though it never saw the full word.

### Word variations FastText handles beautifully

| Word | Shares sub-words with |
|---|---|
| Mango | Mangoes, Mangoed |
| Season | Seasonal, Seasoning, Seasoned |
| Love | Lovely, Loved, Lover, Loveable |

### Full Comparison — All 5 Embeddings

| | BOW | TF-IDF | Word2Vec | GloVe | FastText |
|:---:|:---:|:---:|:---:|:---:|:---:|
| Meaning | ❌ | ❌ | ✅ | ✅ | ✅ |
| Order matters | ❌ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| Sparse vectors | ❌ | ❌ | ✅ | ✅ | ✅ |
| Word importance | ❌ | ✅ | ✅ | ✅ | ✅ |
| Global context | ❌ | ❌ | ❌ | ✅ | ✅ |
| OOV words | ❌ | ❌ | ❌ | ❌ | ✅ |
| Polysemy | ❌ | ❌ | ❌ | ❌ | ❌ |


### What FastText still can't do

*Polysemy - one word and multiple meanings and context dependent meaning*. Fixing polysemy and static embeddings is what led to contextual embeddings like BERT (***Upcoming***) and eventually the Transformer architecture you already have seen in my Tech Blog [1] - however, the that is just the base architecture and as BERT & GPT's came into play, the architecture was refined for better use. 

### One line to remember

***Word2Vec and GloVe learn words. FastText learns the DNA of words — and can reconstruct meaning even for words it has never seen.***

### Layman Analogy

*Imagine you encounter a word in Tamil you've never seen before — but you recognise the root and the suffix. You can make a reasonable guess at the meaning. That's exactly what FastText does — it reads the roots and suffixes of words to understand meaning, even for completely new words.*

---

***Stay Tuned for the upcoming articles on BERT, GPT's and how the transformer architecture evolved as days went by. Its absolutely stunning***
