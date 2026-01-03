import os

# Auto-generate similarity.pkl if missing
if not os.path.exists("similarity.pkl"):
    import generate_similarity

import pickle
import streamlit as st
import requests
import random

# Page Config
st.set_page_config(page_title="NetMirror", layout="wide", page_icon="🎬")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');
    
    /* Global Reset & Font */
    * {
        font-family: 'Roboto', sans-serif;
    }
    
    .stApp {
        background-color: #000000;
        color: white;
    }
    
    /* Remove padding */
    .block-container {
        padding-top: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        max-width: 100%;
    }
    
    /* --- NAVBAR --- */
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 15px 40px;
        background: linear-gradient(180deg, rgba(0,0,0,0.7) 0%, transparent 100%);
        position: fixed;
        width: 100%;
        top: 0;
        z-index: 999;
    }
    
    .logo {
        font-size: 1.5rem;
        font-weight: 900;
        color: #fff;
        margin-right: 40px;
        text-shadow: 0 0 10px rgba(0,0,0,0.5);
    }
    
    .nav-links {
        display: flex;
        gap: 20px;
    }
    
    .nav-item {
        color: #e5e5e5;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        opacity: 0.8;
        transition: opacity 0.3s;
    }
    .nav-item:hover, .nav-item.active {
        opacity: 1;
        font-weight: 700;
    }
    .nav-item.active {
        background-color: #333;
        padding: 5px 15px;
        border-radius: 20px;
    }
    
    .nav-icons {
        display: flex;
        gap: 20px;
        align-items: center;
    }
    
    .user-avatar {
        width: 32px;
        height: 32px;
        background-color: #007bff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }

    /* --- HERO SECTION --- */
    .hero {
        position: relative;
        height: 85vh;
        width: 100%;
        background-size: cover;
        background-position: center top;
        display: flex;
        align-items: center;
        padding-left: 50px;
    }
    
    .hero-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, #000 0%, transparent 60%),
                    linear-gradient(0deg, #000 0%, transparent 50%);
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
        max-width: 600px;
        margin-top: 50px;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 10px;
        text-transform: uppercase;
        background: -webkit-linear-gradient(#fff, #ccc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 20px rgba(0,0,0,0.8);
    }
    
    .hero-badges {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        align-items: center;
    }
    
    .badge {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-gold {
         background: linear-gradient(45deg, #FFD700, #DAA520);
         color: black;
         padding: 5px 10px;
         border-radius: 20px;
         font-weight: 800;
    }
    
    .hero-desc {
        font-size: 1rem;
        line-height: 1.5;
        color: #ddd;
        margin-bottom: 30px;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.8);
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .hero-buttons {
        display: flex;
        gap: 15px;
    }
    
    .btn {
        padding: 10px 25px;
        border-radius: 4px;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        border: none;
    }
    
    .btn-play {
        background-color: #fff;
        color: #000;
    }
    .btn-play:hover {
        background-color: #ddd;
    }
    
    .btn-add {
        background-color: rgba(109, 109, 110, 0.7);
        color: #fff;
    }
    .btn-add:hover {
        background-color: rgba(109, 109, 110, 0.4);
    }

    /* --- RECOMMENDATION SECTION --- */
    .rec-container {
        padding: 20px 40px;
        margin-top: -100px; /* Overlap hero */
        position: relative;
        z-index: 10;
        background: linear-gradient(0deg, #000 80%, transparent);
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 15px;
        color: #fff;
    }
    
    /* Streamlit overrides for horizontal layout mimic */
    div[data-testid="column"] {
        background-color: transparent;
    }

    .movie-card {
        border-radius: 4px;
        overflow: hidden;
        transition: transform 0.3s;
        cursor: pointer;
    }
    .movie-card:hover {
        transform: scale(1.1);
        z-index: 100;
    }
    .movie-card img {
        width: 100%;
        border-radius: 4px;
    }
    
    /* Search Box styling to blend in */
    .search-container {
        max-width: 500px;
        margin-bottom: 20px;
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(0,0,0,0.5) !important;
        border: 1px solid #555 !important;
    }

</style>
""", unsafe_allow_html=True)

# --- NAV BAR ---
st.markdown("""
<div class="navbar">
    <div style="display:flex; align-items:center;">
        <div class="logo">NetMirror</div>
        <div class="nav-links">
            <div class="nav-item active">Home</div>
            <div class="nav-item">Movies</div>
            <div class="nav-item">TV shows</div>
            <div class="nav-item">Watch List</div>
        </div>
    </div>
    <div class="nav-icons">
        <span>🔍</span>
        <div class="user-avatar">👤</div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- DATA LOGIC ---
@st.cache_resource
def load_data():
    movies = pickle.load(open('movie_list.pkl','rb'))
    similarity = pickle.load(open('similarity.pkl','rb'))
    return movies, similarity

movies, similarity = load_data()

# TMDB API Key
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"





def get_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url).json()
        
        poster_path = data.get('poster_path')
        backdrop_path = data.get('backdrop_path')
        overview = data.get('overview', '')
        # Get simplified title (or tagline if exists and strictly desired, but title is safer)
        title = data.get('title', '')
        
        full_poster = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750"
        full_backdrop = f"https://image.tmdb.org/t/p/original/{backdrop_path}" if backdrop_path else "https://via.placeholder.com/1920x1080"
        
        return full_poster, full_backdrop, title, overview
    except:
        return None, None, None, None

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        recommendations = []
        for i in distances[1:7]: # Fetch 6 movies for the row
            movie_id = movies.iloc[i[0]].movie_id
            title = movies.iloc[i[0]].title
            poster, _, _, _ = get_movie_details(movie_id)
            recommendations.append({'title': title, 'poster': poster})
        return recommendations
    except:
        return []

# --- STATE MANAGEMENT ---
if 'selected_movie' not in st.session_state:
    # Default initial movie for the "Hero" section
    # Let's try to find 'Avatar' or something visually stunning in the list
    if 'Avatar' in movies['title'].values:
        st.session_state.selected_movie = 'Avatar'
    else:
        st.session_state.selected_movie = movies['title'].values[0]

if 'search_term' not in st.session_state:
    st.session_state.search_term = st.session_state.selected_movie

# --- HERO SECTION LOGIC ---
# Get details for the currently active movie (either default or searched)
current_movie_row = movies[movies['title'] == st.session_state.selected_movie]
if not current_movie_row.empty:
    current_id = current_movie_row.iloc[0].movie_id
    poster, backdrop, title, overview = get_movie_details(current_id)
else:
    # Fallback
    poster, backdrop, title, overview = ("https://via.placeholder.com/500x750", "https://via.placeholder.com/1920x1080", "Unknown", "")

# Display Hero
st.markdown(f"""
<div class="hero" style="background-image: url('{backdrop}');">
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <div class="hero-title">{title}</div>
        <div class="hero-badges">
            <span class="badge-gold">EARLY ACCESS</span>
            <span class="badge">ENGLISH</span>
            <span class="badge">U/A 13+</span>
        </div>
        <div class="hero-desc">{overview}</div>
        <div class="hero-buttons">
            <button class="btn btn-play">▶ Watch Now</button>
            <button class="btn btn-add">＋ Add to List</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- MAIN CONTENT AREA ---
st.markdown('<div class="rec-container">', unsafe_allow_html=True)

# Search Bar Interaction
st.markdown('<div class="section-title">Search & Discover</div>', unsafe_allow_html=True)
col_search, _ = st.columns([1,2])
with col_search:
    selected_option = st.selectbox(
        "Find a movie...",
        movies['title'].values,
        index=list(movies['title'].values).index(st.session_state.selected_movie) if st.session_state.selected_movie in movies['title'].values else 0,
        label_visibility="collapsed"
    )

    if selected_option != st.session_state.selected_movie:
        st.session_state.selected_movie = selected_option
        st.rerun()

# Recommendations Row
st.markdown(f'<div class="section-title">Because you watched {st.session_state.selected_movie}</div>', unsafe_allow_html=True)

recs = recommend(st.session_state.selected_movie)
if recs:
    cols = st.columns(len(recs))
    for idx, rec in enumerate(recs):
        with cols[idx]:
            st.markdown(f"""
            <div class="movie-card" title="{rec['title']}">
                <img src="{rec['poster']}">
            </div>
            <div style="font-size:0.8rem; margin-top:5px; color:#ccc;">{rec['title']}</div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
