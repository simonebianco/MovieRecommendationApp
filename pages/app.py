import streamlit as st
import pickle
import pandas as pd
import requests

######## Funzioni ########

def get_poster(movie_id, base_url):
    url = base_url + '{}?api_key=746c1f5078edec9978a35268c2bb5686&language=en-US'.format(movie_id)
    response = requests.get(url)
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']
   
def get_recommandations(movie, df, similarity_matrix, base_url):
    movie_index = df[df['title'] == movie].index[0]
    dist = similarity_matrix[movie_index]
    movies_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:11]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = df.iloc[i[0]].id
        recommended_movies.append(df.iloc[i[0]].title)
        recommended_movies_poster.append(get_poster(movie_id, base_url))
    return recommended_movies, recommended_movies_poster

def get_movie_info(name, movie_df):
    movie_df2 = movie_df[['title', 'director', 'genres', 'cast', 'release_date', 'runtime']]
    st.sidebar.subheader('Title:')
    st.sidebar.write(movie_df2[movie_df2['title'] == name].iloc[0,0])
    st.sidebar.subheader('Director:')
    st.sidebar.write(movie_df2[movie_df2['title'] == name].iloc[0,1])
    st.sidebar.subheader('Genres:')
    st.sidebar.write(movie_df2[movie_df2['title'] == name].iloc[0,2])
    st.sidebar.subheader('Cast:')
    st.sidebar.write(movie_df2[movie_df2['title'] == name].iloc[0,3])
    st.sidebar.subheader('Release_date:')
    st.sidebar.write(movie_df2[movie_df2['title'] == name].iloc[0,4])
    st.sidebar.subheader('Runtime:')
    st.sidebar.write(str(movie_df2[movie_df2['title'] == name].iloc[0,5]))

########################

# base url tmdb api
base_url = 'https://api.themoviedb.org/3/movie/'

# import final dataset
movie_df = pickle.load(open('movies_df.pkl', 'rb'))
movie_df = pd.DataFrame(movie_df)

# get titoli film
titles = movie_df['title'].values

# import similarity matrix
similarity_matrix = pickle.load(open('similarity_matrix.pkl', 'rb'))

# titolo pagina
st.title('Movie Recommendation App')

# box selezione film
selected_film = st.selectbox(
'Insert a film name',
titles
)

# bottone raccomandazioni
if st.checkbox('Recommend'):
    # lista 10 raccomandazioni + chiamata api poster
    recommended_movies, recommended_movies_poster = get_recommandations(selected_film, movie_df, similarity_matrix, base_url)
    # 2 righe con 5 film + bottone informazioni per singolo film
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        check1 = st.button('Info 1')
        if check1:
            get_movie_info(recommended_movies[0], movie_df)
        st.write(recommended_movies[0])
        st.image(recommended_movies_poster[0])
          
    with col2:
        check2 = st.button('Info 2')
        if check2:
            get_movie_info(recommended_movies[1], movie_df)
        st.write(recommended_movies[1])
        st.image(recommended_movies_poster[1])
        
    with col3:
        check3 = st.button('Info 3')
        if check3:
            get_movie_info(recommended_movies[2], movie_df)
        st.write(recommended_movies[2])
        st.image(recommended_movies_poster[2])
    with col4:
        check4 = st.button('Info 4')
        if check4:
            get_movie_info(recommended_movies[3], movie_df)
        st.write(recommended_movies[3])
        st.image(recommended_movies_poster[3])
    with col5:
        check5 = st.button('Info 5')
        if check5:
            get_movie_info(recommended_movies[4], movie_df) 
        st.write(recommended_movies[4])
        st.image(recommended_movies_poster[4])

    col6, col7, col8, col9, col10 = st.columns(5)
    with col6:
        check6 = st.button('Info 6')
        if check6:
            get_movie_info(recommended_movies[5], movie_df) 
        st.write(recommended_movies[5])
        st.image(recommended_movies_poster[5])
    with col7:
        check7 = st.button('Info 7')
        if check7:
            get_movie_info(recommended_movies[6], movie_df)
        st.write(recommended_movies[6])
        st.image(recommended_movies_poster[6])
    with col8:
        check8 = st.button('Info 8')
        if check8:
            get_movie_info(recommended_movies[7], movie_df) 
        st.write(recommended_movies[7])
        st.image(recommended_movies_poster[7])
    with col9:
        check9 = st.button('Info 9')
        if check9:
            get_movie_info(recommended_movies[8], movie_df)
        st.write(recommended_movies[8])
        st.image(recommended_movies_poster[8])
    with col10:
        check10 = st.button('Info 10')
        if check10:
            get_movie_info(recommended_movies[9], movie_df)
        st.write(recommended_movies[9])
        st.image(recommended_movies_poster[9])

        
  
