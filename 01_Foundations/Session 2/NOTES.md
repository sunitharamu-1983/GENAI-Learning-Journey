# **Session 2 - Apr 5, 2026**
Early State NLP and Basic Legendary search engine explanation is provided below

## NLP Pipeline (Search Engine Example): 
*The instructor used a search engine to illustrate NLP steps:*

  - **Crawling:** Bots scan web pages. (**Data Collection**) 
  - **Indexing:** Extract and store text/data for fast retrieval. (**Organize Data**)
  - **Scoring:** Assign a score to each document. (**Measure Relevance**)
  - **Ranking:** Algorithms order results by relevance (e.g. PageRank, BM25). (**Initial Ordering**)
  - **Re-Ranking:** Uses deep models and re-orders results. (**Refine Results**)
  - **Stop Words:** Very common words (e.g. “the”, “is”) usually carry little meaning. Search engines use **predefined stop-word lists** or statistical measures (like low TF-IDF weight) to filter them out. Modern NLP models may also *implicitly* learn that these are less informative.  
  - **Stemming vs. Lemmatization:** Both reduce words to a base form. *Stemming* bluntly chops suffixes (e.g. “running”→“run”); *lemmatization* uses vocabulary/grammar (e.g. “better”→“good”) to get the proper dictionary form.  
  - **Part-of-Speech (POS) Tagging:** Automatically labeling words with their grammatical role (noun, verb, etc.). E.g., tagging “park” as noun or verb depending on context. This helps understanding sentence structure.
  - **TF-IDF:**
    - ***TF:*** - Term Frequency - How often a word appears in a document
    - ***IDF:*** - Inverse Document Frequency - How rare a word is across all the documents
    - ***TF & IDF*** - Combined gives the importance score that is how frequent and how rare
  - **Semantics:** Meaning Matching

## Google Colab Setup: 
The instructor demonstrated how to set up and use Google Colaboratory, including connecting to Google Drive, accessing GPU resources, and the free tier limitations (12.7 GB RAM, 107 GB disk space).

## NLP Pipeline Implementation
*The class walked through building a search engine step-by-step:*

  -  **Parsing:** Using BeautifulSoup to extract text from HTML pages
  -  **Tokenization:** Converting text to lowercase and splitting into individual words
  -  **Stop Words Removal:** Using NLTK library to remove common English words (179 stop words)
  -  **Stemming vs Lemmatization:** Comparing rule-based stemming (Porter Stemmer) with dictionary-based lemmatization using WordNet
  -  **Inverted Index Creation:** Building a word-to-document mapping for efficient search
  -  **TF-IDF Explanation:** The instructor is currently explaining Term Frequency-Inverse Document Frequency (TF-IDF) scoring:
  -  **Term Frequency:** How often a word appears in a document divided by total words in that document
  -  **Inverse Document Frequency:** Measures how rare or common a word is across all documents
      -  ***The combination helps identify relevant documents for search queries***
  
  - **TF-IDF Scoring:** Currently explaining Term Frequency-Inverse Document Frequency, which ranks documents by:
      - How often a word appears in a specific document (TF)
      - How rare that word is across all documents (IDF)
      - Multiplying these scores to find the most relevant results
      - The instructor is using a sample dataset of 10 documents about pizza recipes to demonstrate these concepts with live coding examples.
   
## Limitation of TF-IDF
   - It doesn't understand context or meaning - only word occurrence. This led to discussion of why modern search engines use more advanced techniques like embeddings for semantic understanding.
   - The instructor demonstrated all concepts with practical coding examples using a 10-document dataset about pizza recipes.
   - **Context and Meaning:** TF-IDF only considers word occurrence frequency in documents and across the corpus, but does not understand the meaning or context of what the user is searching for. For example, when searching for "automobile," it would rank a document containing that exact word higher, but miss relevant documents about "car racing" or "vehicle maintenance" that are contextually related.
   - **Word Order:** TF-IDF does not consider the order of words in a sentence. For example, "dog bites the man" and "man bites the dog" have completely different meanings, but TF-IDF would give them the same score since they contain the same words.
   - **Stop Words Problem:** Removing stop words (like "NOT") during preprocessing can change the meaning of sentences significantly, which is problematic when context matters. The instructor mentioned that with modern embedding techniques, stop words are no longer removed.
   - **Out of Vocabulary (OOV):** If a word doesn't exist in the inverted index, TF-IDF returns nothing. For example, if the documents are about pizza but someone searches for "cricket" or uses a misspelling like "TIST" instead of "pizza," the system won't find any results even if similar content exists.

## TF-IDF Detailed Explanation
Based on the meeting transcript, here is Noor's detailed explanation of TF (Term Frequency) and IDF (Inverse Document Frequency):

- **Term Frequency (TF):**
TF is the number of times a word appears in a document divided by the total number of words in that document. For example, if a document has 10 words and the word "pizza" occurs 1 time, then TF = 1/10 = 0.10. This calculation is done on a document-by-document basis, not across the entire corpus. The division by total words normalizes for document length - a 1,000 word document would naturally have higher counts than a 10-word document, so we care about proportion, not raw count.

- **Inverse Document Frequency (IDF):**
IDF considers the word across the entire corpus (all documents). The formula is: log(total number of documents / number of documents containing that word). For example, if there are 10 total documents and "pizza" appears in 7 of them, IDF = log(10/7). The log is used as a mathematical convention because when dealing with search engines, the numerator can be trillions of documents, and dividing by a small number would create huge numbers. The log keeps the values manageable. When IDF is low, the word is very common across documents. When IDF is high, the word is rare across documents.

- **TF-IDF Score:**
You multiply TF × IDF for each word in each document. When TF-IDF is high, it means the word appears often in this particular document AND is rare globally - making it very relevant. For a search query with multiple words, you calculate TF-IDF for each word, add them together for each document, then sort by the highest scores to rank the search results.

Noor also mentioned that sometimes the formula uses log(1 + N/n) instead of just log(N/n) - this is called "smooth IDF" to avoid getting zero when a word appears in all documents (since log(1) = 0).

## Modern Approach
The instructor emphasized that TF-IDF is a legacy technique. Modern search engines use embeddings and transformers that understand context, word order, and semantic meaning without requiring preprocessing like stop word removal or stemming. These newer techniques will be covered in upcoming classes.
