import os
import pandas as pd
import requests

# 1. Dataset download logic at the VERY TOP
MOVIES_URL = "https://raw.githubusercontent.com/nikbearbrown/INFO_6105_Data_Science/master/datasets/tmdb_5000_movies.csv"
CREDITS_URL = "https://raw.githubusercontent.com/nikbearbrown/INFO_6105_Data_Science/master/datasets/tmdb_5000_credits.csv"

if not os.path.exists("tmdb_5000_movies.csv"):
    r = requests.get(MOVIES_URL)
    with open("tmdb_5000_movies.csv", "wb") as f:
        f.write(r.content)

if not os.path.exists("tmdb_5000_credits.csv"):
    r = requests.get(CREDITS_URL)
    with open("tmdb_5000_credits.csv", "wb") as f:
        f.write(r.content)

import numpy as np
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def process_data():
    # 3. process_data() ONLY reads CSVs
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")
    
    movies = movies.merge(credits, on='movie_id')
    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    movies.dropna(inplace=True)

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
import pickle
pickle.dump(similarity, open("similarity.pkl", "wb"))
