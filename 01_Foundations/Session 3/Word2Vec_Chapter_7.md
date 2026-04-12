# Word2Vec & FastText - Difference

Yes, **Word2Vec and FastText are different**, although **FastText is technically an extension** of the Word2Vec skip-gram model.

The fundamental differences between the two are as follows:

### **1. Unit of Representation**
*   **Word2Vec:** It treats each word in the vocabulary as an **atomic unit**, meaning it assigns a distinct vector to each word without considering its internal structure.
*   **FastText:** It represents each word as a **"bag of character n-grams"**. For example, with $n=3$, the word "where" is broken down into sub-units like `<wh`, `whe`, `her`, `ere`, `re>` and the special sequence `<where>`. The final vector for the word is the **sum of these n-gram representations**.

### **2. Handling Out-of-Vocabulary (OOV) Words**
*   **Word2Vec:** A major limitation is its inability to infer vectors for **unfamiliar words** that did not appear in the training data.
*   **FastText:** Because it uses subword information, it can generate valid representations for **OOV words** by summing the vectors of the character n-grams it recognises within the new word. This allows the model to "guess" the meaning of a word based on its prefixes, suffixes, or roots.

### **3. Performance on Morphologically Rich Languages**
*   **Word2Vec:** It struggles with languages like **German, Arabic, or Russian**, where words have many inflected forms or cases, as it treats every variation (e.g., "reading" vs. "read") as a completely separate entity.
*   **FastText:** It excels in these languages because it exploits **character-level similarities**. For example, in German, it can recognize the relationship between "Tischtennis" (table tennis) and "Tennis" because they share common n-grams, whereas Word2Vec would not automatically link them unless they appeared in similar contexts.

### **4. Computational Requirements and Results**
*   **Speed:** FastText is approximately **1.5x slower to train** than Word2Vec because it must process multiple n-grams for every single word. For instance, one test showed a thread processing 105k words per second for FastText compared to 145k for Word2Vec.
*   **Transparency:** Like Word2Vec, FastText is considered a **"black box"** compared to legacy techniques like TF-IDF, but it offers far superior results for **synonyms, word order, and rare words**.

In summary, while Word2Vec was a breakthrough in learning word relationships through context, **FastText improved upon it by looking inside the words**, making it much more robust for rare terms and complex languages.
