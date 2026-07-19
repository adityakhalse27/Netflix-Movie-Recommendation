import streamlit as st
import pickle
import requests


# =========================
# TMDB API KEY
# =========================

API_KEY = "56e72d4ad8e148f3b1797111bff304d4"


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Aditya Netflix AI",
    page_icon="🎬",
    layout="wide"
)


# =========================
# CSS
# =========================

st.markdown(
"""
<style>

.stApp{

background:
linear-gradient(
rgba(0,0,0,0.75),
rgba(0,0,0,0.95)
),
url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba");

background-size:cover;
background-attachment:fixed;

color:white;

}


.hero{

text-align:center;
padding:50px;

}


.hero h1{

font-size:65px;
color:#E50914;

}


.hero h2{

font-size:35px;
color:white;

}


.movie-card{

background:rgba(20,20,20,0.85);

padding:20px;

border-radius:20px;

text-align:center;

height:480px;

transition:0.3s;

}


.movie-card:hover{

transform:scale(1.05);

}


.rating{

color:#FFD700;

font-size:20px;

}


.sidebar-title{

color:#E50914;

}

</style>
""",
unsafe_allow_html=True
)



# =========================
# LOAD DATA
# =========================

@st.cache_data
def load_movies():

    return pickle.load(
        open(
            "movies.pkl",
            "rb"
        )
    )


@st.cache_resource
def load_similarity():

    return pickle.load(
        open(
            "similarity.pkl",
            "rb"
        )
    )


movies = load_movies()

similarity = load_similarity()



# =========================
# TMDB DETAILS
# =========================

def get_details(title):

    url="https://api.themoviedb.org/3/search/movie"


    params={

        "api_key":API_KEY,

        "query":title

    }


    response=requests.get(
        url,
        params=params
    )


    data=response.json()


    if data.get("results"):


        movie=data["results"][0]


        poster=movie.get(
            "poster_path"
        )


        if poster:

            poster=(
                "https://image.tmdb.org/t/p/w500"
                +
                poster
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

        "overview":"No Data"

    }




# =========================
# RECOMMENDATION MODEL
# =========================

def recommend(movie):


    index=movies[
        movies["title"]==movie
    ].index[0]


    distance=similarity[index]


    movies_list=sorted(
        enumerate(distance),
        reverse=True,
        key=lambda x:x[1]
    )[1:7]


    result=[]


    for i,score in movies_list:


        result.append({

            "title":
            movies.iloc[i]["title"],


            "score":
            round(
                score*100,
                2
            )

        })


    return result




# =========================
# HEADER
# =========================

st.markdown(
"""
<div class="hero">

<h1>ADITYA'S NETFLIX AI 🎬</h1>

<h2>Movie Recommendation Universe</h2>

<p>
Powered by Machine Learning + TMDB API
</p>

</div>

""",
unsafe_allow_html=True
)




# =========================
# SEARCH
# =========================

st.sidebar.title(
"🔍 Search Movie"
)


search=st.sidebar.text_input(
"Enter Movie Name"
)



if search:


    result=movies[
        movies["title"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]


    st.sidebar.write(
        result["title"].head(10)
    )




# =========================
# ANALYTICS
# =========================

st.subheader(
"📊 Movie Analytics"
)


c1,c2,c3=st.columns(3)


c1.metric(
"Total Movies",
len(movies)
)


c2.metric(
"Algorithm",
"Cosine Similarity"
)


c3.metric(
"Developer",
"Aditya"
)




# =========================
# SELECT MOVIE
# =========================

st.subheader(
"🍿 Select Movie"
)


selected=st.selectbox(

"Choose",

movies["title"].values

)



if st.button(
"🚀 Recommend"
):


    recommendations=recommend(
        selected
    )


    st.subheader(
    "🔥 Recommended Movies"
    )


    cols=st.columns(3)


    for col,item in zip(
        cols*2,
        recommendations
    ):


        with col:


            details=get_details(
                item["title"]
            )


            st.markdown(
            "<div class='movie-card'>",
            unsafe_allow_html=True
            )


            if details["poster"]:

                st.image(
                    details["poster"],
                    width=180
                )


            st.write(
                "🎬",
                item["title"]
            )


            st.markdown(
            f"""
            <p class="rating">
            ⭐ {details["rating"]}
            </p>
            """,
            unsafe_allow_html=True
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
            "Story"
            ):

                st.write(
                    details["overview"]
                )


            st.markdown(
            "</div>",
            unsafe_allow_html=True
            )




# =========================
# FOOTER
# =========================

st.markdown(
"""
---
🚀 Built by Aditya Khalse  
Python | Machine Learning | Streamlit | TMDB API
"""
)