# NetMirror: Movie Recommendation System

A premium, Netflix-style movie recommendation web application powered by Machine Learning.
Designed to help users find similar movies based on their viewing preferences using the TMDB 5000 Movie Dataset.

## Features

- **Cinematic UI**: Dark mode ("True Black"), immersive hero banners, and horizontal scrolling lists.
- **Content-Based Filtering**: Recommendation algorithm using Cosine Similarity on specialized movie tags (genres, keywords, cast, crew).
- **Auto-healing Model**: Includes a dedicated script to regenerate the model files from the raw dataset.
- **Live Data**: Fetches poster and backdrop images dynamically via the TMDB API.

## Tech Stack

- **Frontend**: Streamlit
- **Machine Learning**: Scikit-Learn (CountVectorizer, Cosine Similarity)
- **Data Manipulation**: Pandas, NumPy
- **API Integration**: Python Requests (TMDB)

## Setup & Installation

Follow these steps to set up the project locally.

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Movies-Recommendation-System
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Dataset Setup (Crucial Step)
This project requires the **TMDB 5000 Movie Dataset** to build the recommendation engine.
1. Download `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` from [Kaggle](https://www.kaggle.com/tmdb/tmdb-movie-metadata).
2. Place both CSV files in the **root directory** of this project.

### 4. Generate Models
Run the generation script to create the necessary `.pkl` files (`movie_list.pkl` and `similarity.pkl`).
```bash
python generate_similarity.py
```
*Note: This process may take a minute as it vectorizes 5000+ movies.*

### 5. Run the Application
```bash
streamlit run main.py
```

## Project Structure

- `main.py`: The Streamlit web application.
- `generate_similarity.py`: ETL pipeline that cleans data and generates ML models.
- `EDA_TMDB_Movie_Recommender.ipynb`: Exploratory Data Analysis notebook.
- `requirements.txt`: Project dependencies.
- `*.pkl`: Generated model files (ignored by git).
