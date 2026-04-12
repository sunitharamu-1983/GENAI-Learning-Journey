# Chapter - 6: FASTTESXT Explanation

**FastText** is an extension of the Word2Vec skip-gram model that represents words as a **sum of their subword units**, specifically character **n-grams**. While traditional models like Word2Vec treat words as atomic units and assign a distinct vector to each one, FastText takes into account the **internal structure of words**, allowing it to capture morphological information that other models ignore.

### Core Mechanism: Subword Information
Instead of learning a vector for the whole word only, FastText breaks words down into smaller pieces:
*   **Character n-grams:** A word is represented as a "bag" of its character sequences. For example, if $n=3$, the word "where" would be broken into the n-grams `<wh`, `whe`, `her`, `ere`, and `re>`. 
*   **Boundary Symbols:** Special symbols `<` and `>` are added to the start and end of words to distinguish **prefixes and suffixes** from other character sequences (e.g., `<her>` as the word "her" is distinct from the tri-gram `her` inside "where").
*   **The Full Word:** The original word itself (e.g., `<where>`) is also included in the set of n-grams to ensure the model still learns a representation for the complete term.
*   **Summation:** The final vector for a word is the **sum of all its n-gram vectors**.

### Solving the "Out-of-Vocabulary" Problem
A major limitation of standard Word2Vec is its inability to infer vectors for **unfamiliar words** (words not seen during training). FastText solves this by using its subword logic: even if the model has never seen a specific word, it can still construct a vector for it by **averaging the vectors of the character n-grams** it contains. This makes the model highly effective for **rare words** and technical vocabulary.

### Key Benefits and Performance
*   **Morphologically Rich Languages:** FastText significantly outperforms Word2Vec for languages with complex grammar and many word forms, such as **Czech, German, Russian, Turkish, or Finnish**. 
*   **Small Datasets:** The model is more robust to limited data. For instance, FastText trained on only 5% of a German Wikipedia dataset has been shown to achieve better performance than a standard CBOW model trained on the full dataset.
*   **Syntactic Accuracy:** Because it "understands" how words are built (suffixes, prefixes, and roots), it performs much better on **syntactic tasks** (like identifying plurals or verb tenses) than models that ignore subword data.
*   **Implementation:** In the **Gensim** library, FastText is available as a specific model that uses a **hashing function** (FNV-1a) to efficiently map n-grams to a fixed number of memory buckets, keeping the memory footprint manageable.
