import pandas as pd
import numpy as np
import ast
import pickle
import os
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def process_data():
    print("Checking for dataset files...")
    
    if not os.path.exists('tmdb_5000_movies.csv') or not os.path.exists('tmdb_5000_credits.csv'):
        print("Error: Dataset files not found!")
        print("Please download 'tmdb_5000_movies.csv' and 'tmdb_5000_credits.csv' from Kaggle.")
        print("Place them in the root directory of this project.")
        sys.exit(1)

    print("Loading csv files...")
    movies = pd.read_csv('tmdb_5000_movies.csv')
    credits = pd.read_csv('tmdb_5000_credits.csv')

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
    # 1. Process Data
    print("Starting data processing...")
    try:
        new_df = process_data()
        print(f"Data processed. Movies count: {new_df.shape[0]}")
    except Exception as e:
        print(f"Failed to process data: {e}")
        return

    # 2. Save Movie List
    print("Saving movie_list.pkl...")
    pickle.dump(new_df, open('movie_list.pkl','wb'))

    # 3. Generate Similarity Matrix
    print("Generating similarity matrix (this may take a moment)...")
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(new_df['tags']).toarray()
    similarity = cosine_similarity(vector)

    # 4. Save Similarity
    print("Saving similarity.pkl...")
    pickle.dump(similarity, open('similarity.pkl','wb'))
    
    print("Success! All models generated.")

if __name__ == "__main__":
    generate_models()
else:
    # When imported, also run the generation
    generate_models()

