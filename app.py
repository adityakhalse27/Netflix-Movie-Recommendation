import streamlit as st
import pickle
import pandas as pd
import requests


# ==========================
# TMDB API KEY
# ==========================

API_KEY = "56e72d4ad8e148f3b1797111bff304d4"


# ==========================
# Page Config
# ==========================

st.set_page_config(
    page_title="Netflix Movie Recommendation",
    page_icon="🎬",
    layout="wide"
)


# ==========================
# Netflix CSS
# ==========================

st.markdown(
"""
<style>

.stApp{
    background:#000000;
    color:white;
}

h1{
    color:#E50914;
    text-align:center;
}

.movie-card{

    background:#141414;
    padding:15px;
    border-radius:15px;
    text-align:center;

}

</style>

""",
unsafe_allow_html=True
)



# ==========================
# Load Files
# ==========================

@st.cache_data
def load_movies():

    return pickle.load(
        open("movies.pkl","rb")
    )


@st.cache_resource
def load_similarity():

    return pickle.load(
        open("similarity.pkl","rb")
    )


movies = load_movies()

similarity = load_similarity()



# ==========================
# TMDB Function
# ==========================

def get_movie_details(movie_name):

    url = "https://api.themoviedb.org/3/search/movie"


    params = {

        "api_key": API_KEY,

        "query": movie_name

    }


    response = requests.get(
        url,
        params=params
    )


    data = response.json()


    if data.get("results"):


        movie = data["results"][0]


        poster = movie.get(
            "poster_path"
        )


        if poster:

            poster = (
                "https://image.tmdb.org/t/p/w500"
                + poster
            )


        return {

            "poster":poster,

            "rating":
            movie.get(
                "vote_average",
                "N/A"
            ),

            "date":
            movie.get(
                "release_date",
                "N/A"
            ),

            "overview":
            movie.get(
                "overview",
                "No description"
            )

        }


    return {

        "poster":None,
        "rating":"N/A",
        "date":"N/A",
        "overview":"No data"

    }



# ==========================
# Recommendation Function
# ==========================

def recommend(movie):


    index = movies[
        movies["title"]==movie
    ].index[0]


    distances = similarity[index]


    movie_list = sorted(
        enumerate(distances),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]


    result=[]


    for i,score in movie_list:


        result.append({

            "name":
            movies.iloc[i]["title"],


            "score":
            round(score*100,2)

        })


    return result



# ==========================
# Header
# ==========================


st.title(
"🎬 Netflix Movie Recommendation System"
)


st.write(
"AI Based Movie Recommendation using Machine Learning"
)



# ==========================
# Search
# ==========================

search = st.sidebar.text_input(
"🔍 Search Movie"
)


if search:


    result = movies[
        movies["title"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]


    st.sidebar.write(
        "Results"
    )


    for movie in result.head(5)["title"]:

        st.sidebar.write(
            movie
        )



# ==========================
# Select Movie
# ==========================


selected_movie = st.selectbox(

    "Select Movie",

    movies["title"].values

)



if st.button(
    "Recommend Movies",
    key="recommend_btn"
):


    recommendations = recommend(
        selected_movie
    )


    st.subheader(
        "🔥 Recommended Movies"
    )


    cols = st.columns(5)


    for col,item in zip(
        cols,
        recommendations
    ):


        with col:


            details = get_movie_details(
                item["name"]
            )


            st.markdown(
            "<div class='movie-card'>",
            unsafe_allow_html=True
            )


            if details["poster"]:


                st.image(
                    details["poster"],
                    width=130
                )


            st.write(
                "🎬",
                item["name"]
            )


            st.write(
                "⭐",
                details["rating"]
            )


            st.write(
                "📅",
                details["date"]
            )


            st.write(
                "🤖 Match:",
                item["score"],
                "%"
            )


            with st.expander(
                "Overview"
            ):

                st.write(
                    details["overview"]
                )


            st.markdown(
            "</div>",
            unsafe_allow_html=True
            )



# Footer

st.markdown(
"""
---
Made with Python + Streamlit + Machine Learning 🤖
"""
)