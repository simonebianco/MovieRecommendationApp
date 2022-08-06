import streamlit as st
import pickle
import pandas as pd

# load dataset finale
movie_df = pickle.load(open('movies_df.pkl', 'rb'))
movie_df = pd.DataFrame(movie_df)

# conversione intero numero voti
movie_df['vote_count'] = movie_df['vote_count'].astype('int')

# 5 film più votati (numero)
most_voted_count = movie_df.sort_values(by=['vote_count'], ascending=False).iloc[:6, :].reset_index()

# 5 film più votati (media)
most_voted_avg = movie_df.sort_values(by=['vote_average'], ascending=False).iloc[:6, :].reset_index()

# titolo - voto
most_voted_count = most_voted_count[['title', 'vote_count']]
most_voted_avg = most_voted_avg[['title', 'vote_average']]

# titolo pagina
st.title('Movie Recommendation App')

# descrizione app
st.subheader('App')
text_app = 'The application is built using the Streamlit module with Python and is intended to provide recommendations on 10 movies with higher similarity than the one entered by the user. The final dataset was processed by merging the individual csvs, and only the first 2000 highest rated films were kept. The data were then pre-processed and vectorized to allow calculation of the cosine similarity among the 2000 films presents which is used as a measure for recommendation'
st.write(text_app)

# descrizione dati
st.subheader('Dataset')
text_dataset = 'These files pubblished on Kaggle contain metadata for all 45,000 movies listed in the Full MovieLens Dataset. The dataset consists of movies released on or before July 2017. Data points include cast, crew, plot keywords, budget, revenue, posters, release dates, languages, production companies, countries, TMDB vote counts and vote averages. This dataset is an ensemble of data collected from TMDB and GroupLens. The Movie Details, Credits and Keywords have been collected from the TMDB Open API. The Movie Links and Ratings have been obtained from the Official GroupLens website.'
st.write(text_dataset)

# link Kaggle data
st.write('Link available at: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset')

# tabelle top 5
st.subheader('Top 5 movies most voted (count)')
st.write(most_voted_count)

st.subheader('Top 5 movies most voted (avg)')
st.write(most_voted_avg)