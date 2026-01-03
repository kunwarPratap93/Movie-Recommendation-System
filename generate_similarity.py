# TMDB Movie Recommendation - Data Generation Script
import os
import sys

# Check if we can use existing pickle file
if os.path.exists("movie_list.pkl"):
    print("Found existing movie_list.pkl - using it to generate similarity matrix only...")
    import pickle
    import pandas as pd
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Load existing movie list
    print("Loading movie_list.pkl...")
    movies = pickle.load(open("movie_list.pkl", "rb"))
    
    # Generate similarity matrix
    print("Generating similarity matrix (this may take a moment)...")
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(movies['tags']).toarray()
    similarity = cosine_similarity(vector)
    
    # Save similarity
    print("Saving similarity.pkl...")
    pickle.dump(similarity, open("similarity.pkl", "wb"))
    
    print("Success! Similarity matrix generated.")
    sys.exit(0)

# If movie_list.pkl doesn't exist, try to download and process datasets
import pandas as pd
import numpy as np
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("""
================================================================================
TMDB Dataset Required
================================================================================
This project needs the TMDB 5000 Movie Dataset.

Please follow these steps:
1. Download from Kaggle: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
2. Extract 'tmdb_5000_movies.csv' and 'tmdb_5000_credits.csv'
3. Place both files in the project root directory
4. Run this script again: python generate_similarity.py

Alternatively, use the existing movie_list.pkl if available.
================================================================================
""")

if not os.path.exists("tmdb_5000_movies.csv") or not os.path.exists("tmdb_5000_credits.csv"):
    print("ERROR: CSV files not found!")
    sys.exit(1)

def process_data():
    print("Loading csv files...")
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")

    print("Merging datasets...")
    movies = movies.merge(credits, on='title')

    # key columns
    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    movies.dropna(inplace=True)

    print("Preprocessing data...")
    def convert(text):
        L = []
        for i in ast.literal_eval(text):
            L.append(i['name']) 
        return L 

    def convert3(text):
        L = []
        counter = 0
        for i in ast.literal_eval(text):
            if counter < 3:
                L.append(i['name'])
            counter+=1
        return L 

    def fetch_director(text):
        L = []
        for i in ast.literal_eval(text):
            if i['job'] == 'Director':
                L.append(i['name'])
        return L 

    def collapse(L):
        L1 = []
        for i in L:
            L1.append(i.replace(" ",""))
        return L1

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert3)
    movies['crew'] = movies['crew'].apply(fetch_director)

    movies['cast'] = movies['cast'].apply(collapse)
    movies['crew'] = movies['crew'].apply(collapse)
    movies['genres'] = movies['genres'].apply(collapse)
    movies['keywords'] = movies['keywords'].apply(collapse)

    movies['overview'] = movies['overview'].apply(lambda x:x.split())
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

    new = movies.drop(columns=['overview','genres','keywords','cast','crew'])
    new['tags'] = new['tags'].apply(lambda x: " ".join(x))

    return new

def generate_models():
    print("Starting data processing...")
    try:
        new_df = process_data()
        print(f"Data processed. Movies count: {new_df.shape[0]}")
    except Exception as e:
        print(f"Failed to process data: {e}")
        return

    # Save Movie List
    print("Saving movie_list.pkl...")
    pickle.dump(new_df, open("movie_list.pkl", "wb"))

    # Generate Similarity Matrix
    print("Generating similarity matrix (this may take a moment)...")
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(new_df['tags']).toarray()
    similarity = cosine_similarity(vector)

    # Save Similarity
    print("Saving similarity.pkl...")
    pickle.dump(similarity, open("similarity.pkl", "wb"))
    
    print("Success! All models generated.")

if __name__ == "__main__":
    generate_models()
else:
    # When imported, also run the generation
    generate_models()
