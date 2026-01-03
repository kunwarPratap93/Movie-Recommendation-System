# Live Demo
https://movie-recommendation-system-2ti2crc8a9n9b3xdi5es24.streamlit.app/

# Movie Recommendation System

A premium, Netflix-style movie recommendation web application powered by Machine Learning and the TMDB API.
This project demonstrates the implementation of a sophisticated recommendation engine packed into a "True Black" cinematic interface.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)
![API](https://img.shields.io/badge/API-TMDB-green)
![License](https://img.shields.io/badge/License-MIT-purple)

## 🎥 Project Overview

This application is designed to replicate the experience of premium streaming services. It goes beyond simple list-based recommendations by providing an immersive "Hero" section, rich metadata, and a dynamic, responsive UI. The core machine learning engine analyzes thousands of movies to surface hidden gems that mathematically match the user's taste.

## ✨ Features

- **Cinematic UI**: Features a bespoke "True Black" dark mode, hero banners with dynamic backdrops, and horizontal scrolling lists inspired by Netflix.
- **Smart Recommendations**: Uses Natural Language Processing (NLP) techniques to analyze movie genes, keywords, cast, and crew.
- **Dynamic Content**: Fetches real-time posters, ratings, and backdrops via the TMDB API.
- **Search & Discovery**: specialized search functionality that adapts to user selection.
- **Robust Architecture**: Built with a clear separation between data processing (`generate_similarity.py`) and application logic (`main.py`).

## 🧠 Recommendation Techniques

This project explores and implements several core recommendation strategies:

### 1. Content-Based Filtering (Implemented)
The primary engine of the system. We utilize **Cosine Similarity** on a vectorized "tags" matrix.
- **How it works**: We combine movie overviews, genres, keywords, cast, and director into a single "gene" string for each movie.
- **Vectorization**: These strings are converted into high-dimensional vectors using `CountVectorizer`.
- **Similarity**: We calculate the angle between these vectors. Movies with smaller angles are "closer" in content space.

### 2. Collaborative Filtering (Concept)
While Content-Based filtering focuses on item properties, Collaborative Filtering focuses on user behavior.
- **User-Based**: "Users who liked Movie A also liked Movie B."
- **Item-Based**: "Users who liked Movie A tended to rate Movie B highly."
*The system is architected to support this by extending the dataset with user id/rating matrices.*

### 3. Hybrid Approach (Concept)
The "Holy Grail" of recommendation systems. The design allows for a hybrid module that calculates a weighted average between Content-Based scores and Collaborative scores, providing accurate suggestions even for new users (Cold Start problem) while personalizing for power users.

### 4. User Rating Personalization
We utilize TMDB's `vote_average` and `vote_count` to filter and sort high-quality recommendations, ensuring users aren't recommended poorly-rated obscure films unless they specifically search for them.

## 🛠 Technologies & Frameworks

- **Web Framework**: Streamlit (Python)
- **Data Source**: TMDB API & Kaggle Dataset
- **Machine Learning**: Scikit-Learn
- **Data Processing**: Pandas, NumPy
- **Environment**: Python 3.x

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites
- Python installed on your local machine.
- Pip package manager.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Data Setup**
   - Download `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` from Kaggle.
   - Place them in the root directory.

### Generating the Model
This project decouples model generation from runtime to ensure performance and stay within GitHub's file limits.

```bash
python generate_similarity.py
```
*This may take a few moments as it processes 5000 movies.*

### Running the Application
Launch the interface:

```bash
streamlit run main.py
```

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgements

- **TMDB** for the fantastic API.
- **Streamlit** for the rapid application framework.
- The Python Data Science community.
