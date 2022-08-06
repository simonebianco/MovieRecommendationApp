import pandas as pd
from functions import *
import warnings; warnings.simplefilter('ignore')
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# read single datasets
credits = pd.read_csv('data/credits.csv')
keywords = pd.read_csv('data/keywords.csv')
links = pd.read_csv('data/links.csv')
movies_metadata = pd.read_csv('data/movies_metadata.csv')

# features
features = ['id', 'title','genres', 'overview','cast', 'crew', 'keywords', 'production_companies', 'release_date', 'runtime', 'vote_average', 'vote_count']

# preparazione dataset finale
df = prepare_dataset(credits, keywords, links, movies_metadata, features)

# teniamo solo i 3000 film con il più altro numero di voti
df = df.sort_values(by=['vote_count'], ascending=False).iloc[:3000, :].reset_index()

# rimozione colonna vecchi indici
df.drop(columns='index', inplace=True)

# features per vectorization
vect_features = ['id', 'title','genres', 'overview','cast', 'director', 'keywords']

# preparazione dataset vectorization
df_to_vect = vectorize_dataset(df, vect_features)

# vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')

# una riga per film, una colonna per parola (5000), gli elementi sono la frequenza delle parola per film
# (3000, 5000)
vectors = cv.fit_transform(df_to_vect['features']).toarray()

# cosine_similarity
# coseno similatitá per un film con tutti gli altri
# (3000, 3000)
similarity_matrix = cosine_similarity(vectors) 

cv.get_feature_names() # lista parole considerate

# 10 film con più alta similarità
film = 'Inception'
get_recommendations(film, similarity_matrix, df)

# export df file
pickle.dump(df.to_dict(), open('movies_df.pkl', 'wb'))

# export matrice similarity
pickle.dump(similarity_matrix, open('similarity_matrix.pkl', 'wb'))


