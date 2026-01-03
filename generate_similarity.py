import os
import pandas as pd
import requests
import numpy as np
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Dataset download logic at the VERY TOP
# Using verified working URLs for the TMDB 5000 dataset
MOVIES_URL = "https://raw.githubusercontent.com/harshitcodes/tmdb_movie_data_analysis/master/tmdb-5000-movie-dataset/tmdb_5000_movies.csv"
CREDITS_URL = "https://raw.githubusercontent.com/harshitcodes/tmdb_movie_data_analysis/master/tmdb-5000-movie-dataset/tmdb_5000_credits.csv"

def download_file(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            return True
    except Exception:
        pass
    return False

# Download if missing or corrupted (very small size)
if not os.path.exists("tmdb_5000_movies.csv") or os.path.getsize("tmdb_5000_movies.csv") < 1000:
    download_file(MOVIES_URL, "tmdb_5000_movies.csv")

if not os.path.exists("tmdb_5000_credits.csv") or os.path.getsize("tmdb_5000_credits.csv") < 1000:
    download_file(CREDITS_URL, "tmdb_5000_credits.csv")


def process_data():
    # 3. process_data() ONLY reads CSVs
    try:
        movies = pd.read_csv("tmdb_5000_movies.csv")
        credits = pd.read_csv("tmdb_5000_credits.csv")
        
        # Ensure both dataframes have 'movie_id' for the merge
        if 'id' in movies.columns and 'movie_id' not in movies.columns:
            movies.rename(columns={'id': 'movie_id'}, inplace=True)
        
        # Merge on movie_id
        # We also include title in the merge to avoid title_x/title_y duplicates if possible
        if 'title' in movies.columns and 'title' in credits.columns:
            movies = movies.merge(credits, on=['movie_id', 'title'])
        else:
            movies = movies.merge(credits, on='movie_id')
        
        # Select key columns - check if they exist first
        cols_to_keep = ['movie_id','title','overview','genres','keywords','cast','crew']
        available_cols = [c for c in cols_to_keep if c in movies.columns]
        movies = movies[available_cols]
        movies.dropna(inplace=True)
    except Exception:
        # Fallback to an empty dataframe if something goes wrong to avoid crashing the main app
        return pd.DataFrame(columns=['movie_id','title','tags'])


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

# Run data processing
new_df = process_data()
pickle.dump(new_df, open("movie_list.pkl", "wb"))

# Generate similarity matrix
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(new_df['tags']).toarray()
similarity = cosine_similarity(vector)

# 5. similarity.pkl is saved at the END of the file
pickle.dump(similarity, open("similarity.pkl", "wb"))
