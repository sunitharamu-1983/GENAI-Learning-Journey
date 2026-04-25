# Cosine Similarity

Cosine Similarity measures the angular closeness between two vectors. It doesn't care about size — only direction. 
- Two vectors pointing in the same direction = similar.
- Two vectors pointing in opposite directions = dissimilar.]

## Why Cosine?

Cosine measures how aligned two vectors are — regardless of their size. 

```
Angle = 0 (Identical Direction) - Cos 0 = 1, Sin 0 = 0
Angle = 90 (Perpendicular) - Cos 90 = 0, Sin 90 = 1
Angle = 180 (Opposite) - Cos 180 = -1, Sin 180 = 0
```

**See the problem with Sine immediately?**

- When two vectors are identical — sin(0°) = 0 — Sine says "not similar at all!" ❌
- When two vectors are perpendicular — sin(90°) = 1 — Sine says "perfectly similar!" ❌

*This is precisely why we use COSINE formula to determine the direction of the vectors. Though vectors have a different magnitude, if in the same direction, they will be called similar.*

*Sine peaks at perpendicularity — the exact moment two things have nothing in common. Cosine peaks at alignment — the exact moment two things are identical. Similarity needs Cosine.*

---

## The Formula

**Cosine Similarity = (A · B) / (||A|| × ||B||)**

- **A · B** = Dot product of vectors A and B
- **||A||** = Magnitude of vector A
- **||B||** = Magnitude of vector B

*The dot product captures how aligned the vectors are. Dividing by the magnitudes removes the effect of size — so two short vectors and two long vectors pointing in the same direction both score 1.*

---

## The Score and What it Means

| Score | Meaning |
|---|---|
| **1** | Identical — vectors point in exactly the same direction |
| **0** | No similarity — vectors are perpendicular |
| **-1** | Opposite — vectors point in completely opposite directions |

---

## Sample Calculation

```
Example:
S1 — "I love India"
S2 — "I love Mango"
S3 — "Mango is a seasonal fruit"
```

### Step 1 — Build the BOW Vectors

Vocabulary: I, love, India, Mango, is, a, seasonal, fruit

| | I | love | India | Mango | is | a | seasonal | fruit |
|---|---|---|---|---|---|---|---|---|
| **S1** | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| **S2** | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| **S3** | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |

---

### Step 2 — Apply the Formula

#### Comparison 1 — S1 vs S2

```
Dot Product:
(1×1) + (1×1) + (1×0) + (0×1) + (0×0) + (0×0) + (0×0) + (0×0) = 2

Magnitude of S1:
√(1²+1²+1²+0²+0²+0²+0²+0²) = √3 = 1.732

Magnitude of S2:
√(1²+1²+0²+1²+0²+0²+0²+0²) = √3 = 1.732

Cosine Similarity = 2 / (1.732 × 1.732) = 2 / 3 = 0.667
```

*S1 and S2 share "I" and "love" but differ on "India" vs "Mango." Score of 0.667 = moderately similar.*

---

#### Comparison 2 — S1 vs S3

```
Dot Product:
(1×0) + (1×0) + (1×0) + (0×1) + (0×1) + (0×1) + (0×1) + (0×1) = 0

Cosine Similarity = 0 / (1.732 × 2.236) = 0.000
```

*S1 and S3 share no common words at all. Score of 0 = completely dissimilar.*

---

#### Comparison 3 — S2 vs S3

```
Dot Product:
(1×0) + (1×0) + (0×0) + (1×1) + (0×1) + (0×1) + (0×1) + (0×1) = 1

Magnitude of S3:
√(0²+0²+0²+1²+1²+1²+1²+1²) = √5 = 2.236

Cosine Similarity = 1 / (1.732 × 2.236) = 1 / 3.873 = 0.258
```

*S2 and S3 share only "Mango." Score of 0.258 = weakly similar.*

---

### Summary of Results

| Comparison | Score | Interpretation |
|---|---|---|
| S1 vs S2 | **0.667** | Moderately similar — share "I love" |
| S1 vs S3 | **0.000** | No similarity — no common words |
| S2 vs S3 | **0.258** | Weakly similar — share only "Mango" |

---

## Where is Cosine Similarity used in AI?

- **Semantic Search** — finding documents that mean the same thing even if they use different words
- **Recommendation Systems** — finding similar items based on vector closeness — I did try developing a Product recommender with the backend as FastAPI and front end as React JS and cosine similarity helped me identify the similar products😊

---

## Why NOT Cosine Similarity for training?

*Cosine Similarity cannot capture loss during training because it only measures direction, not magnitude. During training, the model needs to know HOW WRONG it was — not just the direction.*

---

## One line to remember

*Cosine Similarity doesn't ask "how big are you?" — it asks "which way are you pointing?" And in the world of text similarity, direction is everything.*

---

## Closing Comments

***Cosine Similarity is the bridge between embeddings and real-world applications like search, recommendation and RAG. The vectors your embeddings produce are only as useful as the similarity measure that compares them.***

