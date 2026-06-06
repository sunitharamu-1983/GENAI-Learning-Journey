# Chapter - 1 : Understanding Word2Vec and Distributed Word Representations

#### Introduction to Word2Vec
**Word2Vec** is a widely used algorithm based on **shallow neural networks** designed to learn relationships between words automatically from large volumes of unannotated plain text,. Unlike traditional Natural Language Processing (NLP) techniques that treat words as atomic units or indices in a vocabulary, Word2Vec represents words as **continuous vectors** in a lower-dimensional space,. The model ensures that word-vectors for terms with similar meanings are positioned close to each other in this vector space, while those with different meanings are distant. This allows for the discovery of **linear relationships**, such as the famous example: `vec("king") - vec("man") + vec("woman") =~ vec("queen")`,.

#### Moving Beyond Bag-of-Words
The Word2Vec model was developed as an improvement over the traditional **Bag-of-Words (BoW)** model. In a BoW model, documents are transformed into fixed-length vectors of integers where each element counts word occurrences. While effective for some tasks, BoW has two primary weaknesses: 
1.  **Loss of Order:** It disregards word order (e.g., "John likes Mary" and "Mary likes John" result in identical vectors).
2.  **Lack of Semantic Meaning:** It does not learn the underlying meaning of words, meaning the distance between vectors does not reflect semantic differences.

Word2Vec addresses these by focusing on the **contextual meaning** of words through distributed representations,.

#### Core Model Architectures
There are two primary architectures implemented within the Word2Vec framework:

1.  **Skip-gram (SG):** This model is designed to predict the **surrounding context words** given a single input word,. It uses a one-hidden-layer neural network where projection weights from a virtual one-hot encoding are interpreted as the word embeddings. The training task involves maximizing the classification of nearby words within a certain range.
2.  **Continuous Bag-of-Words (CBOW):** Conversely, CBOW predicts a **target center word** based on the average of multiple input context words,. Because it uses an average, the specific order of words in the history does not influence the projection, hence the name "bag-of-words".

While both models are "shallow" (having only one hidden layer), they are highly efficient and can be trained on billions of words in less than a day,.

#### Training and Optimization
Training Word2Vec is an **unsupervised task**, and the quality of the resulting vectors depends on several parameters:
*   **`vector_size`:** The number of dimensions in the N-dimensional space. While higher values (typically in the hundreds) require more data, they generally lead to more accurate models,.
*   **`min_count`:** This parameter prunes the dictionary by ignoring infrequent words (e.g., typos or rare terms) that lack enough data for meaningful training.
*   **`workers`:** This allows for **parallelization**, speeding up training on multicore machines,.

For optimization, Word2Vec often employs **Hierarchical Softmax** or **Negative Sampling**. Hierarchical Softmax uses a **Huffman binary tree** to represent the vocabulary, assigning shorter binary codes to frequent words to reduce the number of output units that must be evaluated,.

#### Linear Regularities and Algebra
One of the most remarkable discoveries regarding Word2Vec is that these vectors capture **syntactic and semantic regularities** through simple algebraic operations,. For example, the model can solve analogies like "Athens is to Greece as Oslo is to Norway". This is achieved by computing a vector (e.g., `vector("biggest") - vector("big") + vector("small")`) and searching for the closest word vector (e.g., "smallest") using **cosine distance**.

#### Practical Implementation and Constraints
In the **Gensim** library, the `Word2Vec` model is highly optimized using C routines. A key feature is **data streaming**, which allows the model to process large corpora directly from a disk or network without loading the entire dataset into RAM,. The model parameters are stored as **NumPy arrays**, and memory requirements are dominated by these matrices (calculated as `#vocabulary * vector_size * 4 bytes * 3 matrices`).

#### Limitations and the Evolution to Subword Information
Despite its power, a significant limitation of standard Word2Vec is its inability to infer vectors for **out-of-vocabulary (OOV) words**. Because it assigns a distinct vector to each word, it ignores the internal morphology of words—a major drawback for morphologically rich languages like Finnish or Turkish,. 

To address this, follow-up models like **FastText** represent each word as a **bag of character n-grams**. In this approach, a word is the sum of its character n-gram vectors (e.g., the word "where" with n=3 is represented by `<wh`, `whe`, `her`, `ere`, `re>`),. This allows the model to compute valid representations for unseen words based on their subword components.
