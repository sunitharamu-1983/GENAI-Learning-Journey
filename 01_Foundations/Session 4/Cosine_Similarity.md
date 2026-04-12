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

## Cosine Similarity Formula:
- Cosine Similarity = (A · B) / (|A| × |B|)

Where:

- A · B is the dot product (multiply corresponding elements and add them)
- |A| and |B| are the magnitudes (square root of sum of squared elements)

## Applying the formula:

- **Dot Product (Numerator):**
  - (1 × 2) + (1 × 2) = 2 + 2 = 4

- **Magnitude of A:**
  - √(1² + 1²) = √(1 + 1) = √2

- **Magnitude of B:**
  - √(2² + 2²) = √(4 + 4) = √8

- **Final Calculation:**
  - 4 / (√2 × √8) = 4 / √16 = 4 / 4 = 1
  - **Result:** The cosine similarity is 1, which means the documents are perfectly similar (same direction/meaning), even though Document B has larger values. This shows that cosine similarity cares about direction, not magnitude.
