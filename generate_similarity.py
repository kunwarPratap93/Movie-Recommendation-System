# Auto-generate model files for movie recommendation
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# If movie_list.pkl exists, just generate similarity.pkl from it
if os.path.exists("movie_list.pkl"):
    movies = pickle.load(open("movie_list.pkl", "rb"))
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(movies['tags']).toarray()
    similarity = cosine_similarity(vector)
    pickle.dump(similarity, open("similarity.pkl", "wb"))
else:
    # Full processing from CSV files
    import pandas as pd 
    import numpy as np
    import ast
    
    def process_data():
        movies = pd.read_csv("tmdb_5000_movies.csv")
        credits = pd.read_csv("tmdb_5000_credits.csv")
        movies = movies.merge(credits, on='title')
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
    
    new_df = process_data()
    pickle.dump(new_df, open("movie_list.pkl", "wb"))
    
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(new_df['tags']).toarray()
    similarity = cosine_similarity(vector)
    pickle.dump(similarity, open("similarity.pkl", "wb"))
