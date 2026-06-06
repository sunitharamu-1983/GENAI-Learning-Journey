# Does embedding have a pipeline and how is word2vec related to embedding?

## Embedding:
- ***Embedding*** is the process of converting words to vectors (numbers) where each number holds meaning and context of the word or sentence. As explained in the meeting, "embedding is just giving a number to a word, and that number holds a name ." The key difference from older methods like bag of words or TF-IDF is that embeddings capture the understanding and meaning of words, not just their frequency.

## Word2Vec and Embedding:
- ***Word2vec*** is a specific method/model for creating embeddings. In the meeting, they discussed using a pre-trained word2vec model (trained on Google News with about 100 billion words) that already has vectors calculated for words. As mentioned, "It is already calculated. We are not doing anything. It is not doing any sort of on-flight task. It is just taking up... giving the vector for each words, whatever it has been trained."

## Pipeline:
While the meeting doesn't explicitly mention a formal "pipeline" for embeddings, the process discussed involves:

- Tokenization (splitting text into words)
- Converting each word to its vector representation using the embedding model
- For documents, combining word vectors (like taking averages) to create document-level vectors
- Using these vectors for similarity calculations (cosine similarity)
- The meeting demonstrated that word2vec is essentially a tool that provides pre-trained embeddings, which are then used as the foundation for various NLP tasks like similarity search and recommendation systems.
