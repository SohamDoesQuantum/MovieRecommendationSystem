import streamlit as st
import pandas as pd
import pickle
import os
import gdown

st.title("Movie Recommendation System")

# Function to download large files from Google Drive
@st.cache_resource # Prevents downloading it every time a user clicks a button
def load_data():
    # Replace these IDs with YOUR actual file IDs from the Google Drive links
    movies_file_id = 'https://1drv.ms/u/c/BDC93B19D04E2812/IQAYekEsIzouRYuVY57ND0LoAX6Rj9OSg3pTr1srxkgcHgI?e=wycxri'
    similarity_file_id = 'https://1drv.ms/u/c/BDC93B19D04E2812/IQD7Y8vxsNRVQ6OuH5igx0YUAQD5fqpys6RaibbBXN1trHU?e=ZrpPy4'
    
    if not os.path.exists('movies_dict.pkl'):
        gdown.download(id=movies_file_id, output='movies_dict.pkl', quiet=True)
        
    if not os.path.exists('similarity.pkl'):
        gdown.download(id=similarity_file_id, output='similarity.pkl', quiet=True)

    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    
    return pd.DataFrame(movies_dict), similarity

# Load the data
movies, similarity = load_data()

# Dropdown menu for movie selection
selected_movie_name = st.selectbox(
    'Type or select a movie to get recommendations:',
    movies['title'].values
)


# 3. Recommendation logic adapted from your notebook function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    # Sort and grab top 5 recommendations
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# 4. Button to trigger recommendations
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for movie in recommendations:
        st.write(movie)
