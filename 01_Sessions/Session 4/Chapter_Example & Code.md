# Content Based Recommendation

## Requirement is to build a content-based recommendation engine for movies, similar to what Netflix or Amazon Prime uses

### Here's a quick summary of the requirement:

**Goal:** Create a movie recommendation system that suggests similar movies based on what a user has watched.

### Approach:

- Use a dataset of 1000 movies from IMDB containing information like movie title, genre, overview/description, director, cast (stars), ratings, etc.
    
- Convert the movie information (text data) into numerical vectors using embeddings.
    
- Calculate similarity between movies using cosine similarity (not Euclidean distance, as discussed extensively in the session - cosine similarity is better for text-based comparisons because it focuses on direction/meaning rather than magnitude).
    
- When a user watches a movie (e.g., Dark Knight 1), find the most similar movies based on cosine similarity scores and recommend them (e.g., Dark Knight 2).

**Key Point:** *This is content-based recommendation, meaning it recommends based purely on the similarity of movie content/metadata, not on user behavior patterns or other users' preferences.*

---

***The instructor mentioned there are other types like user-based and item-based recommendations, but this exercise focuses on content-based using the movie metadata provided in the IMDB dataset.***

---

# Explanation of the code

The session focused on building a movie recommendation system using word embeddings and cosine similarity. Here's what was covered:

1. **Data Preparation:** Started with an IMDB dataset containing 1000 movies with information like title, genre, overview, director, and cast.

2. **Feature Combination:** Combined relevant columns (genre, overview, director, star1, star2, star3, star4) into a single "combined_features" column for each movie.

3. **Tokenization:** Split the combined features text into individual words using the split() function, creating a tokenized_data variable.

4. **Word Embeddings:** Used a pre-trained Word2Vec model (Google News with 300-dimensional vectors) to get embeddings for each word.

5. **Document to Vector Conversion:** Created a function that:
   - Iterates through each document (movie)
    - For each word in the document, retrieves its embedding from the Word2Vec model
    - Adds all word embeddings together
    - Divides by the number of words to get an average
    - This creates a 300-dimensional vector for each movie
    - Final output: 1000 movies x 300 dimensions

7. **Cosine Similarity:** Used sklearn's cosine_similarity function to calculate similarity scores between all movie pairs, creating a similarity matrix.

***Recommendation: For a given movie (like Shawshank Redemption), the code sorts similarity scores in descending order to find the most similar movies.***

The instructor noted that preprocessing (lowercase conversion, punctuation removal) was skipped initially to focus on the embedding and similarity concepts, but could be added later for better results.
