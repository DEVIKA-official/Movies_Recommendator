import streamlit as st
import pickle
import pandas as pd
from imdb import IMDb


# Function to get movie poster from IMDb using IMDbPY
def get_movie_poster(movie_title):
    ia = IMDb()
    search_results = ia.search_movie(movie_title)

    if search_results:
        movie = search_results[0]
        ia.update(movie)

        if 'cover url' in movie:
            return movie['cover url']
    return None


def Recommend(movie):
    try:
        movie_index = movies[movies['Title'] == movie].index[0]  # Find the index of the movie
        distances = similarity[movie_index]  # Get the similarity distances for the movie
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
                      1:10]  # Sort distances and get top 10
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i[0]].Title)
        return recommended_movies

    except IndexError:
        print(f"Movie '{movie}' not found in the dataset.")
        return None  # Handle the case where the movie is not found


# Open the pickle file in binary read mode
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Extract movie titles for selectbox
movie_titles = movies['Title'].values

st.title('Movies Recommender')
selected_movie_name = st.selectbox(
    'What Would You Like To Watch Today...🧐 ?',
    movie_titles
)

if st.button('Recommend'):
    recommendations = Recommend(selected_movie_name)
    if recommendations:
        cols = st.columns(len(recommendations))  # Create columns for each recommendation
        for col, movie in zip(cols, recommendations):
            with col:
                st.markdown(f"<h3 style='text-align: center;'>{movie}</h3>", unsafe_allow_html=True)
                poster_url = get_movie_poster(movie)
                if poster_url:
                    st.image(poster_url, use_column_width=True)
                else:
                    st.write("Poster not found.")
    else:
        st.write("No recommendations available for the selected movie.")

# Add custom CSS to improve the layout
st.markdown("""
    <style>
    .stImage {
        display: flex;
        justify-content: center;
    }
    .stImage img {
        max-height: 300px;
        margin: 0 auto;
    }
    .stColumn {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 2px;
    }
    .stColumn > div {
        text-align: center;
    }
    h3 {
        margin-top: 0;
        margin-bottom: 2px;
        font-size: 1em;
    }
    </style>
    """, unsafe_allow_html=True)
