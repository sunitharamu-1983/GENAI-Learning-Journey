# Cardinal Variables vs One Hot Encoding - Complete Guide (Sunitha Ramu)

## 1. Cardinal Variables = "Real Numbers" ✅
**Definition**: Numbers where math actually means something. You can add, subtract, multiply, and the results make real-world sense.

**Examples**:
Age: 43 → "43 is 2x bigger than 21" ✓
₹5 lakhs salary → "5 lakhs is 2x 2.5 lakhs" ✓
65kg weight → "65kg > 50kg by 15kg" ✓
Distance: 10km → "10km is twice 5km" ✓
Temperature: 37°C → "37°C is hotter than 25°C by 12°" ✓


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
├── Age: 43 years (CARDINAL → use raw number 43)
├── Salary: ₹8L (CARDINAL → use raw number 800000)
├── Department: IT (CATEGORY → One Hot encode)
├── City: Coimbatore (CATEGORY → One Hot encode)


**Final Table Ready for AI Model**:

| Age | Salary  | Dept_IT | Dept_HR | City_Coimbatore | City_Chennai |
|-----|---------|---------|---------|-----------------|--------------|
| 43  | 800000  | **1**   | 0       | **1**           | 0            |
| 35  | 600000  | 0       | **1**   | 0               | **1**        |
| 48  | 950000  | **1**   | 0       | 0               | 0            |

## 5. Quick Decision Tree
Can I do real math on this?
├── YES → Cardinal → Use raw numbers directly
└── NO → Category → One Hot encode first


**Examples Test**:

| Data          | Math Test     | Type      | Action           |
|---------------|---------------|-----------|------------------|
| Age 43 × 2    | = 86 years ✓ | **CARDINAL** | Use raw         |
| Coimbatore ×2 | = ?? ❌      | **CATEGORY** | One Hot encode  |
| ₹5L × 2       | = ₹10L ✓    | **CARDINAL** | Use raw         |
| Apple × 2     | = ?? ❌      | **CATEGORY** | One Hot encode  |

## 6. Classroom Questions to Ask Tomorrow
1. "When do we skip One Hot encoding entirely?"
2. "What's the difference between One Hot vs Label Encoding?"
3. "How do we handle categories with 1000+ options (high cardinality)?"
4. "Does One Hot work the same in NLP vs tabular data?"

---

**Created by**: Sunitha Ramu (IT Professional, Coimbatore, Tamil Nadu)  
**With**: Perps (Perplexity AI Companion)  
**Date**: April 11, 2026  
**Purpose**: AI Training Notes - GitHub Repository Ready  
**Version**: 1.0 - Complete & Self-Contained
