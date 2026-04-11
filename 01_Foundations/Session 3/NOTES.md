# Cardinal Variables vs One Hot Encoding

## 1. Cardinal Variables = "Real Numbers" ✅
**Definition**: Numbers where math actually means something. You can add, subtract, multiply, and the results make real-world sense.

**Examples**:
- Age: 43 → "43 is 2x bigger than 21" ✓
- ₹5 lakhs salary → "5 lakhs is 2x 2.5 lakhs" ✓
- 65kg weight → "65kg > 50kg by 15kg" ✓
- Distance: 10km → "10km is twice 5km" ✓
- Temperature: 37°C → "37°C is hotter than 25°C by 12°" ✓


**Key Test**: "Can I multiply this by 2 and it still makes sense?"
- **Yes** → Cardinal variable (use directly in AI models)
- **No** → Category (needs encoding)

## 2. Categories/Word Labels = "Non-Cardinal" ❌
**Examples**: Coimbatore, Apple, IT, Female, Monday, Red, HR Department

**The Problem**:
Wrong encoding: Coimbatore=1, Chennai=2, Mumbai=3
→ Computer thinks: "Chennai > Coimbatore" (FALSE!)


## 3. One Hot Encoding = "YES/NO Switches" 🔄
**Purpose**: Convert word labels into computer-friendly numbers WITHOUT fake math order.

**Fruit Example**:

| Fruit  | Price | Apple | Mango | Banana |
|--------|-------|-------|-------|--------|
| Apple  | 50    | **1** | 0     | 0      |
| Mango  | 80    | 0     | **1** | 0      |
| Banana | 60    | 0     | 0     | **1**  |

**City Example** (Your Context):

| City        | Salary  | Coimbatore | Chennai | Mumbai |
|-------------|---------|------------|---------|--------|
| Coimbatore  | 800000  | **1**      | 0       | 0      |
| Chennai     | 900000  | 0          | **1**   | 0      |
| Mumbai      | 1200000 | 0          | 0       | **1**  |

## 4. Real-World AI Training Example (Your IT Work)

**Employee Dataset**:
1. Age: 43 years (CARDINAL → use raw number 43)
2. Salary: ₹8L (CARDINAL → use raw number 800000)
3. Department: IT (CATEGORY → One Hot encode)
4. City: Coimbatore (CATEGORY → One Hot encode)


**Final Table Ready for AI Model**:

| Age | Salary  | Dept_IT | Dept_HR | City_Coimbatore | City_Chennai |
|-----|---------|---------|---------|-----------------|--------------|
| 43  | 800000  | **1**   | 0       | **1**           | 0            |
| 35  | 600000  | 0       | **1**   | 0               | **1**        |
| 48  | 950000  | **1**   | 0       | 0               | 0            |

## 5. Quick Decision Tree
Can I do real math on this?
- YES → Cardinal → Use raw numbers directly
- NO → Category → One Hot encode first


**Examples Test**:

| Data          | Math Test     | Type      | Action           |
|---------------|---------------|-----------|------------------|
| Age 43 × 2    | = 86 years ✓ | **CARDINAL** | Use raw         |
| Coimbatore ×2 | = ?? ❌      | **CATEGORY** | One Hot encode  |
| ₹5L × 2       | = ₹10L ✓    | **CARDINAL** | Use raw         |
| Apple × 2     | = ?? ❌      | **CATEGORY** | One Hot encode  |

--- 
## Bag of Words (BoW)

**Bag of Words (BoW)** = Imagine dumping all words from a sentence into a shopping bag, then counting how many of each you have. Order doesn't matter, just the counts.

***Dead Simple Example***
- Sentence 1: "Cat sat mat"
→ Bag: cat=1, sat=1, mat=1

- Sentence 2: "Cat cat sat"  
→ Bag: cat=2, sat=1, mat=0

**How It Looks as Numbers:**

| Sentence      | Cat        | Sat      | Mat           |
|---------------|---------------|-----------|------------------|
| "Cat sat mat"   | 1 | 1 | 1         |
| "Cat cat sat" | 2      | 1 | 0 |
| "Mat only"      | 0   |0 | 1     |

**Key Points:**
- Ignores order: "Cat sat mat" = "Mat sat cat" (same vector)
- Counts frequency: More apples = higher number
- Fixed size: Always same length (vocab size)
- Simple but dumb: No grammar, no meaning, just counts

**Another Example:**
- Employee review: "Great work team excellent"
→ BoW: great=1, work=1, team=1, excellent=1

- Bad review: "Poor work slow team"
→ BoW: poor=1, work=1, slow=1, team=1

Raw Text
    ↓
1. **One Hot Encoding** (1980s) 
   → Each word = single YES/NO vector
   → "Apple" = [1,0,0], "Banana" = [0,1,0]
   → **Problem**: Ignores word order, massive vectors

2. **Bag of Words** (1990s)
   → Counts word frequency, ignores order  
   → "Apple apple banana" = [2,1,0]
   → **Problem**: Still ignores order/meaning

3. **TF-IDF** (2000s)
   → Bag of Words + rarity weighting
   → Rare words get higher scores

4. **Word2Vec** (2013) → **Words as nearby vectors**
5. **BERT/GPT** (2018+) → **Context-aware embeddings**

## Quick Comparison Table - Text-to-Numbers Evolution

| Method          | Word Order? | Counts Freq? | Vector Size | Use Case                    |
|-----------------|-------------|--------------|-------------|-----------------------------|
| **One Hot**     | ❌ No       | ❌ No        | **Huge**    | Small vocab, simple labels  |
| **Bag of Words**| ❌ No       | ✅ Yes       | Medium      | Document classification     |
| **TF-IDF**      | ❌ No       | ✅ Weighted  | Medium      | Search engines, ranking     |
| **Word2Vec**    | ✅ Partial  | ❌ No        | **Small**   | Word similarity, clustering |
| **BERT**        | ✅ Full     | ✅ Context   | Adaptive    | Modern NLP, chatbots        |
