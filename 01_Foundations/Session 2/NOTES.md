## **Session 2 - Apr 5, 2026**

# NLP Pipeline (Search Engine Example): 
*The instructor used a search engine to illustrate NLP steps:*

  - **Crawling:** Bots scan web pages.  
  - **Indexing:** Extract and store text/data for fast retrieval.  
  - **Ranking:** Algorithms order results by relevance (e.g. PageRank, BM25).  
  - **Stop Words:** Very common words (e.g. “the”, “is”) usually carry little meaning. Search engines use **predefined stop-word lists** or statistical measures (like low TF-IDF weight) to filter them out. Modern NLP models may also *implicitly* learn that these are less informative.  
  - **Stemming vs. Lemmatization:** Both reduce words to a base form. *Stemming* bluntly chops suffixes (e.g. “running”→“run”); *lemmatization* uses vocabulary/grammar (e.g. “better”→“good”) to get the proper dictionary form.  
  - **Part-of-Speech (POS) Tagging:** Automatically labeling words with their grammatical role (noun, verb, etc.). E.g., tagging “park” as noun or verb depending on context. This helps understanding sentence structure.
