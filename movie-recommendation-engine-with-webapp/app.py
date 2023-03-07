import streamlit as st
import pickle5 as pickel
import pandas as pd
import requests;

st.title("Movie recommendation system")

movie = pickel.load(open("movie.pkl",'rb'))
cosine_similarity = pickel.load(open("cosine_similarity.pkl", 'rb'))
indicies = pickel.load(open("indicies.pkl", 'rb'))
cosine_sim2 = pickel.load(open("cosine_sim2.pkl", 'rb'))
movie = movie[['title','id']]
selected_movie_name = st.selectbox(
        "Select Movie Name",
        movie
    )  

def fetch_poster(movie_id):
   response = requests.get(
       "https://api.themoviedb.org/3/movie/{}?api_key=fe43f397d82d22ae399c811a1e76b157".format(movie_id))
   data = response.json()
   try:
        return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']
   except:
       return 'movie-poster.jpeg'


def get_movie_recomendation_content_base(title, cosine_similarity=cosine_similarity, indicies=indicies):
    idx = indicies[title.lower().replace(" ", "")]
    cosine_similarity_items = list(enumerate(cosine_similarity[idx]))

    image_list = []
    keys = []

    cosine_similarity_items = sorted(
        cosine_similarity_items, key=lambda x: x[1], reverse=True)
    cosine_similarity_items = cosine_similarity_items[1:11]
    similar_items_index = [i[0] for i in cosine_similarity_items]
    suggestlist =  movie.iloc[similar_items_index]
    data = pd.DataFrame(suggestlist)['title'].values.tolist()

   
    for j in data:
    #    st.text(movie[movie['title'] == j])
       keys.append(movie[movie['title'] ==j ]['id'])
    # st.text(keys)
    for i in keys:
       #st.text(i.values[0])
       im = fetch_poster(i.values[0])
       image_list.append(im)


    return data,image_list


if st.button('Recommend'):
    fetch_poster(11)
    reco,imagelist = get_movie_recomendation_content_base(
        selected_movie_name, cosine_sim2)
    col4, col5, col6 = st.columns(3)
    col1, col2, col3 = st.columns(3)
 

    with col1:
          st.text(reco[0])
          st.image(imagelist[0])

    with col2:
           st.text(reco[1])
           st.image(imagelist[1])

    with col3:
           st.text(reco[2])
           st.image(imagelist[2])
    with col4:
           st.text(reco[3])
           st.image(imagelist[3])

    with col5:
           st.text(reco[4])
           st.image(imagelist[4])

    with col6:
           st.text(reco[5])
           st.image(imagelist[5])
