import ast
from nltk.stem.porter import PorterStemmer

def convert_from_dict(obj):
    L = []
    for i in ast.literal_eval(obj):
        # recupera dal dizionario il valore associato alla chiave nome
        L.append(i['name'])
    return L

def get_actors(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 5:
           # recupera 5 attori dal cast 
            L.append(i['name'])
            counter += 1 
    return L

def get_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
        # recupera il nome del regista
            L.append(i['name'])
    return L

def prepare_dataset(credits, keywords, links, movies_metadata, features):

    # cancella righe errate
    movies_metadata = movies_metadata.drop([19730, 29503, 35587])
    # conversione chiavi id in interi
    credits['id'] = credits['id'].astype('int')
    keywords['id'] = keywords['id'].astype('int')
    movies_metadata['id'] = movies_metadata['id'].astype('int')
    # recupero tmdb id per legame
    links = links[links['tmdbId'].notnull()]['tmdbId'].astype('int')
    # merge dataset
    df = movies_metadata.merge(credits, on='id').merge(keywords, on='id')
    # verifco presenza legame id tmdb
    df = df[df['id'].isin(links)]
    # estrazione features
    df = df[features]
    # rimozione righe senza titolo
    df = df[df['title'].notnull()]
    # gestione valori null
    df["overview"] = df["overview"].fillna('')
    df["release_date"] = df["release_date"].fillna('')
    df["runtime"] = df["runtime"].fillna('')
    # estrazione valori da dizionari
    df["genres"] = df["genres"].apply(convert_from_dict)
    df["production_companies"] = df["production_companies"].apply(convert_from_dict)
    df["keywords"] = df["keywords"].apply(convert_from_dict)
    df["cast"] = df["cast"].apply(get_actors)
    df["crew"] = df["crew"].apply(get_director)
    # creazione stringhe da liste
    df["genres"] = df["genres"].apply(lambda x: ",".join(x)) 
    df["production_companies"] = df["production_companies"].apply(lambda x: ",".join(x)) 
    df["keywords"] = df["keywords"].apply(lambda x: ",".join(x)) 
    df["cast"] = df["cast"].apply(lambda x: ",".join(x)) 
    df["crew"] = df["crew"].apply(lambda x: ",".join(x)) 
    # rename colonna regista
    df.rename(columns={'crew':'director'}, inplace=True)
    # rimozione duplicazioni
    df.drop_duplicates(inplace=True)

    return df

def stem(text):
    ps = PorterStemmer()
    L = []
    for i in text.split():
        # rimozione suffissi parole per eliminare parole diverse con stesso significato
        L.append(ps.stem(i))
    return " ".join(L)

def vectorize_dataset(df, vect_features):

    # feature per similaritá
    df_to_vect = df[vect_features]
    # trasformare stringhe in liste
    df_to_vect['genres'] = df_to_vect['genres'].apply(lambda x: x.split(','))
    df_to_vect['cast'] = df_to_vect['cast'].apply(lambda x: x.split(','))
    df_to_vect['director'] = df_to_vect['director'].apply(lambda x: x.split(','))
    df_to_vect['keywords'] = df_to_vect['keywords'].apply(lambda x: x.split(','))
    df_to_vect['overview'] = df_to_vect['overview'].apply(lambda x: x.split())
    # rimozione spazi per ciascun elemento nelle liste
    df_to_vect['genres'] = df_to_vect['genres'].apply(lambda x: [i.replace(" ", '') for i in x])
    df_to_vect['cast'] = df_to_vect['cast'].apply(lambda x: [i.replace(" ", '') for i in x])
    df_to_vect['director'] = df_to_vect['director'].apply(lambda x: [i.replace(" ", '') for i in x])
    df_to_vect['keywords'] = df_to_vect['keywords'].apply(lambda x: [i.replace(" ", '') for i in x])
    # colonna concatenata features
    df_to_vect['features'] = df_to_vect['genres'] + df_to_vect['cast'] + df_to_vect['director'] + df_to_vect['keywords'] + df_to_vect['overview']
    # dataframe trasformato
    df_to_vect = df_to_vect[['id', 'title', 'features']]
    # singola stringa di attributi
    df_to_vect['features'] = df_to_vect['features'].apply(lambda x: " ".join(x))
    # trasformazioni minuscolo
    df_to_vect['features'] = df_to_vect['features'].apply(lambda x: x.lower())
    # applicazione funzione stem
    df_to_vect['features'] = df_to_vect['features'].apply(stem)

    return df_to_vect

def get_recommendations(movie, similarity_matrix, df):
    # recupero indice film
    movie_index = df[df['title'] == movie].index[0]
    # lista con valori similarità con gli altri film
    dist = similarity_matrix[movie_index]
    # ordinamento descrescente escluso se stesso (similarità 1) per tenere i primi 10
    movies_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:11]
    for i in movies_list:
        print(df.iloc[i[0]].title)    