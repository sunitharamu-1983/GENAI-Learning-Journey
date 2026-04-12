# Chapter - 3: Practical Implementation—Word2Vec Code Examples

Implementing **Word2Vec** is made highly efficient through the **Gensim** library, which provides Pythonic interfaces for training, saving, and querying models. Below are code-level examples derived from the sources to demonstrate how to use these tools.

#### 1. Basic Training and Initialization
The simplest way to initialize and train a model is by passing a list of tokenised sentences directly to the `Word2Vec` constructor.

```python
from gensim.models import Word2Vec

# Define a tiny corpus (list of lists of tokens)
sentences = [["cat", "say", "meow"], ["dog", "say", "woof"]]

# Initialize and train the model
# vector_size: dimensionality of the vectors
# window: maximum distance between current and predicted word
# min_count: ignore words with total frequency lower than this
# workers: number of threads for parallelization
model = Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)
```

#### 2. Accessing Word Vectors and Similarity
Once trained, word vectors are stored in the `model.wv` attribute (a `KeyedVectors` instance).

```python
# Get the numpy vector for a specific word
vector = model.wv['cat']

# Find the 10 most similar words
similar_words = model.wv.most_similar('cat', topn=10)

# Perform vector algebra: King - Man + Woman =~ Queen
# result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'])

# Check which word does not belong in a sequence
odd_one_out = model.wv.doesnt_match(["cat", "dog", "france"])
```

#### 3. Advanced Training Workflow
For larger datasets, it is often better to separate the vocabulary building from the actual training process. This allows for more control over the learning rate and progress.

```python
model = Word2Vec(min_count=1)

# Step 1: Prepare the model vocabulary
model.build_vocab(sentences)

# Step 2: Train the neural weights
model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs)
```

#### 4. Model Persistence (Saving and Loading)
Training can be time-consuming, so saving the model to disk is essential for later use or for resuming training with new data.

```python
# Save the full model (includes hidden weights and vocab tree)
model.save("word2vec.model")

# Load the full model back
model = Word2Vec.load("word2vec.model")

# To save memory, save only the word vectors if further training isn't needed
word_vectors = model.wv
word_vectors.save("word2vec.wordvectors")

# Load back with memory-mapping (read-only, shared across processes)
from gensim.models import KeyedVectors
wv = KeyedVectors.load("word2vec.wordvectors", mmap='r')
```

#### 5. Handling Phrases (Multi-Word Expressions)
Standard Word2Vec treats words as single units. The `Phrases` module can automatically detect common bigrams (like "New_York") to create higher-quality embeddings.

```python
from gensim.models import Phrases

# Train a bigram detector
bigram_transformer = Phrases(sentences)

# Use the transformer to create a model where "words" can be multi-word expressions
model = Word2Vec(bigram_transformer[sentences], min_count=1)
```

#### 6. Using Pre-trained Models
You don't always need to train from scratch. Gensim allows you to download models trained on massive datasets like Google News or Twitter.

```python
import gensim.downloader

# List available pre-trained models
print(list(gensim.downloader.info()['models'].keys()))

# Download 25-dimensional GloVe vectors trained on Twitter data
glove_vectors = gensim.downloader.load('glove-twitter-25')

# Use them just like your own trained vectors
print(glove_vectors.most_similar('twitter'))
```

#### 7. Out-of-Vocabulary (OOV) Prediction
While Word2Vec itself cannot infer vectors for unknown words, it does provide tools to predict the most likely word given a context.

```python
# Predict the most likely center word for a given context
# Note: This is an experimental feature and works best with negative sampling models
predictions = model.predict_output_word(["say", "meow"], topn=5)
```
