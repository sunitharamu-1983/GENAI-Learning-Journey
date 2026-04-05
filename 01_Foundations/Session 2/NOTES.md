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
