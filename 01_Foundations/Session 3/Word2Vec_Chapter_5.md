# Characater N-Grams:

**Character n-grams** are subword units consisting of sequences of $n$ characters extracted from a word. In models like FastText, they are used to represent words as a collection of these smaller parts rather than as a single, atomic unit. This approach allows the system to capture **morphological information**, which is particularly useful for rare words or languages with complex word structures.

### Key Features and Mechanics
*   **Extraction Process:** To create these n-grams, a model typically extracts all character sequences of a specific length range (commonly **$n = 3$ to $6$**). For example, using the word "where" with $n = 3$, the resulting n-grams would be `<wh`, `whe`, `her`, `ere`, and `re>`. 
*   **Boundary Symbols:** Special characters (like `<` and `>`) are added to the beginning and end of the word. These symbols help the model distinguish between a sequence of characters that appears inside a word and one that functions as a **prefix or suffix**. For instance, the tri-gram `<her>` (the word "her") is treated as distinct from the tri-gram `her` found inside the word "where".
*   **The Full Word:** In addition to the smaller slices, the model typically includes the original word itself (e.g., `<where>`) in the set of n-grams to preserve its complete identity.
*   **Vector Summation:** Each unique character n-gram is assigned its own vector representation. To find the final vector for a whole word, the model simply **sums the vectors** of all the n-grams it contains.

### Why Character N-grams are Useful
*   **Handling Rare and New Words:** Because the model learns representations for the "building blocks" of words, it can compute a valid vector for a word it has **never seen before** by summing the vectors of its known n-grams.
*   **Capturing Meaning (Morphemes):** Qualitative analysis shows that the most important n-grams often correspond to **morphemes**—the smallest units of meaning. For example:
    *   In German compound nouns like *Autofahrer* (car driver), the n-grams `auto` and `fahr` are identified as highly significant.
    *   In English, n-grams capture prefixes like `un-` in *unlucky* or suffixes like `-ness` in *kindness*.
    *   In French, they capture verb inflections such as the endings `-ais>` or `-ions>`.
*   **Grammar and Structure:** Longer n-grams (up to $n = 6$) are effective at capturing compound nouns, while shorter ones are useful for identifying grammatical suffixes related to **conjugations and declensions**. However, 2-grams are often considered too short to be informative for semantic tasks because they usually only capture one real character and one boundary symbol.

### Memory Efficiency
Because a massive corpus can contain millions of unique character n-grams, models often use a **hashing function** (specifically the FNV-1a variant). This maps all possible n-grams into a fixed number of "buckets" (e.g., 2 million), which bounds the memory requirements while still allowing the model to share representations across different words.
