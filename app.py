import streamlit as st
import pandas as pd
import pickle
import os
import urllib.request

st.title("Movie Recommendation System")

@st.cache_resource
def load_data():
    movies_url = "https://onedrive.live.com/download?cid=BDC93B19D04E2812&resid=BDC93B19D04E2812%21174246&authkey=AX6Rj9OSg3pTr1srxkgcHgI"
    similarity_url = "https://onedrive.live.com/download?cid=BDC93B19D04E2812&resid=BDC93B19D04E2812%21174317&authkey=AQD5fqpys6RaibbBXN1trHU"
    
    # Force delete broken/empty files from previous failed attempts
    for file in ['movies_dict.pkl', 'similarity.pkl']:
        if os.path.exists(file) and os.path.getsize(file) < 100000:  # If file is too small, it's just broken HTML text
            os.remove(file)
            
    # Download with a User-Agent header so OneDrive allows the direct download
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
    urllib.request.install_opener(opener)

    if not os.path.exists('movies_dict.pkl'):
        with st.spinner("Downloading movies data..."):
            urllib.request.urlretrieve(movies_url, 'movies_dict.pkl')
        
    if not os.path.exists('similarity.pkl'):
        with st.spinner("Downloading similarity matrix (this may take a minute)..."):
            urllib.request.urlretrieve(similarity_url, 'similarity.pkl')

    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    
    return pd.DataFrame(movies_dict), similarity

# Load data smoothly
movies, similarity = load_data()

# Dropdown menu for movie selection
selected_movie_name = st.selectbox(
    'Type or select a movie to get recommendations:',
    movies['title'].values
)

# Recommendation function from your notebook
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    # Grabs top 5 matches
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Button trigger
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for movie in recommendations:
        st.write(movie)
