# Chapter - 8: Doc2Vec

**Doc2Vec is a method to convert an entire document into a vector representation. Here's how it works:**

First, you need Word2Vec embeddings for individual words. Each word has a vector of fixed dimensions (in this case, 300 dimensions).

### To create a document vector:

- Take all the words in the document
- Get the embedding (vector) for each word from the Word2Vec model
- Add all these word vectors together element-wise
- Divide the sum by the total number of words in the document

- For example, if you have two words with vectors:
    - Add them
    - Divide by 2 (number of words):
    - This becomes your document vector
    - The resulting document vector has the same dimensions as the word vectors (300 in this example).

This process is repeated for each document in your dataset, creating a collection of document vectors that can then be used for tasks like finding similar documents using cosine similarity.

***The key point emphasized in the meeting is that the vector size must be the same for both word vectors and document vectors to enable this conversion.***
