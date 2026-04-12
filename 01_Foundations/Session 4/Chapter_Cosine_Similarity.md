# COSINE SIMILARITY

**Based on the context, they are discussing two main formulas:**

## Euclidean Distance Formula:

- For two vectors with points (x1, y1) and (x2, y2)
- Formula: Square root of [(x1 - x2)² + (y1 - y2)²]
- This measures the straight-line distance between two points
- For text/NLP tasks, this is considered less suitable because it focuses on magnitude (how far apart points are) rather than meaning

## Cosine Similarity Formula:
- Formula: (A · B) / (|A| × |B|)
  - Where A · B is the dot product (multiply corresponding elements and add them)
  - |A| is the magnitude of vector A (square root of sum of squared elements)
  - |B| is the magnitude of vector B (square root of sum of squared elements)
  - The result ranges from -1 to 1:
  - 1 means identical/same meaning (0 degree angle)
  - 0 means no relation (90 degree angle)
  - -1 means completely opposite (180 degree angle)

The instructor emphasizes that for NLP and text embeddings, cosine similarity is preferred because it measures the direction/angle between vectors (capturing meaning and context) rather than just the distance. This is important because documents with the same meaning but different lengths would appear far apart using Euclidean distance, but cosine similarity correctly identifies them as similar.

---

## Cosine Similarity - Example

Let's say we have two documents:

- Document A: (1,1)
- Document B: (2,2)

### Cosine Similarity Formula:
- Cosine Similarity = (A · B) / (|A| × |B|)

Where:

- A · B is the dot product (multiply corresponding elements and add them)
- |A| and |B| are the magnitudes (square root of sum of squared elements)

### Applying the formula:

- **Dot Product (Numerator):**
  - (1 × 2) + (1 × 2) = 2 + 2 = 4

- **Magnitude of A:**
  - √(1² + 1²) = √(1 + 1) = √2

- **Magnitude of B:**
  - √(2² + 2²) = √(4 + 4) = √8

- **Final Calculation:**
  - 4 / (√2 × √8) = 4 / √16 = 4 / 4 = 1
  - **Result:** The cosine similarity is 1, which means the documents are perfectly similar (same direction/meaning), even though Document B has larger values. This shows that cosine similarity cares about direction, not magnitude.

---

## Cosine Similarity trumps Euclidean Distance - How? 

Based on the meeting transcript, here are examples showing how cosine similarity trumps Euclidean distance:

### Example 1: Repeated Words

- Document A: "very good" (vector: 1,1)
- Document B: "very good very good" (vector: 2,2)

These documents have the same meaning, just repeated.

- Euclidean distance: √[(2-1)² + (2-1)²] = 1.414 (shows them as different)
- Cosine similarity: 1 (shows them as identical/same meaning)

### Example 2: ML vs AI Documents
- Machine Learning (41 words)
- AI (135 words)
- Football (43 words)
- Tennis (46 words)

### Euclidean distance results:
- ML and AI: 11.958 (far apart)
- ML and Football: 8.6 (closest)
- ML and Tennis: 8.86

***This incorrectly shows ML is most similar to Football, just because their document lengths are similar. But contextually, ML and AI should be most similar.*** 

***Cosine similarity correctly identifies ML and AI as most similar because it focuses on direction/meaning rather than document length.***

---

### Key Point: Euclidean distance is affected by magnitude (how many times words occur), while cosine similarity cares about direction (the meaning/context). For text analysis, meaning matters more than word count, which is why cosine similarity is preferred for NLP tasks.

---

## Count Vectorizer (Bag of Words):

Count Vectorizer is a technique that converts text documents into numerical vectors. It counts how many times each word appears in a document. For example, if you have documents about "ML", "AI", "football", and "tennis", Count Vectorizer creates columns for all unique words and shows the count of each word's occurrence in each document.

***In the meeting example, they showed:***

- Document 0 (ML document): Each unique word gets counted
- Document 1 (AI document): The word "AI" occurred 3 times, "artificial" occurred 4 times
- The vocabulary size was 136 columns (136 unique words across all documents)

### The Process Shown:
- Create a Count Vectorizer object with stop words removed (common words like "the", "is" filtered out)
- Use fit_transform() to convert documents into arrays
- Convert the sparse array to a numpy array, then to a Pandas dataframe for viewing
- Each row represents a document, each column represents a unique word, and the values show occurrence counts

### Key Problem Discussed:
The instructor explained that Count Vectorizer (bag of words) has a limitation - it only captures word frequency, not context or meaning. This is why they were comparing Euclidean distance vs Cosine similarity for measuring document similarity.

---

**The main point was that bag of words gives numbers based on word counts, but these numbers don't hold the contextual meaning that embeddings provide.**
