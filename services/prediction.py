import numpy as np
import pandas as pd
from flask import jsonify
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from services.spotify import get_audio_features_multiple, get_recently_played, get_track_info

# Caminhos dos arquivos de dados
genre_df_path = "music_data/data_by_genres.csv"
year_data_path = "music_data/data_by_year.csv"

# Carregar os dados das músicas

# Transforma as músicas recentemente ouvidas em um DataFrame
def transform_recently_played_to_df(recently_played):
    tracks_info = []

    for item in recently_played['items']:
        track_data = item['track']['track_data']
        audio_features = item['track']['audio_features']

        # Verificar se track_data e audio_features são válidos
        if track_data and audio_features:
            track_info = {
                'valence': audio_features.get('valence'),
                'year': track_data['album']['release_date'][:4] if track_data['album'].get(
                    'release_date') else None,
                'acousticness': audio_features.get('acousticness'),
                'artists': ", ".join([artist['name'] for artist in track_data['artists']]) if track_data.get(
                    'artists') else None,
                'danceability': audio_features.get('danceability'),
                'duration_ms': track_data.get('duration_ms'),
                'energy': audio_features.get('energy'),
                'explicit': track_data.get('explicit'),
                'id': track_data.get('id'),
                'instrumentalness': audio_features.get('instrumentalness'),
                'key': audio_features.get('key'),
                'liveness': audio_features.get('liveness'),
                'loudness': audio_features.get('loudness'),
                'mode': audio_features.get('mode'),
                'name': track_data.get('name'),
                'popularity': track_data.get('popularity'),
                'release_date': track_data['album'].get('release_date'),
                'speechiness': audio_features.get('speechiness'),
                'tempo': audio_features.get('tempo')
            }
            tracks_info.append(track_info)

    user_recent_tracks = pd.DataFrame(tracks_info)
    return user_recent_tracks

# Função para recomendar músicas com base nas músicas ouvidas pelo usuário
def get_top_recommendations(unheard_music_features, heard_music_features, unheard_music, top=10):
    similarities = cosine_similarity(unheard_music_features, heard_music_features)
    similarity_scores = similarities.sum(axis=1)

    unheard_music['similarity'] = similarity_scores
    top_recommendations = unheard_music.sort_values(by='similarity', ascending=False).drop_duplicates(
        subset=['id']).head(top)
    
    recommendation_df = top_recommendations
    return recommendation_df

# Método para obter as músicas recentemente ouvidas pelo usuário com os dados de áudio
def get_recently_played_with_audio_features():
    recently_played = get_recently_played()
    
    track_ids = list(map(lambda x: x['track']['id'], recently_played['items']))
    audio_features = get_audio_features_multiple(track_ids)['audio_features']

    for item in recently_played['items']:
        track_data = get_track_info(item['track']['id'])
        
        if track_data and audio_features:
            item['track']['track_data'] = track_data
            item['track']['audio_features'] = next((x for x in audio_features if x['id'] == item['track']['id']), None)

    return recently_played

# Método para obter recomendações baseadas nas músicas ouvidas pelo usuário
def get_music_recommendation():
    # Obter músicas recentemente ouvidas pelo usuário e transformar em DataFrame
    recently_played_df = transform_recently_played_to_df(get_recently_played_with_audio_features())

    print(recently_played_df.head())

    music_df = pd.read_csv("music_data/music_data.csv")

    # # Alinhar tipos de dados para garantir consistência ao adicionar novas músicas
    for col in music_df.columns:
        if col in recently_played_df.columns:
            recently_played_df[col] = recently_played_df[col].astype(music_df[col].dtype)

    # Identificar e adicionar novas músicas ao DataFrame
    new_tracks = recently_played_df[~recently_played_df['id'].isin(music_df['id'])]
    new_tracks = new_tracks.reindex(columns=music_df.columns, fill_value=np.nan)
    music_df = pd.concat([music_df, new_tracks], ignore_index=True)

    music_features = [
        'valence', 'year', 'acousticness', 'danceability', 'duration_ms',
        'explicit', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo'
    ]

    X = music_df[music_features].select_dtypes(np.number)

    # Pipeline para clustering das músicas
    song_cluster_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('kmeans', KMeans(n_clusters=7, n_init=30, verbose=0))
    ])

    song_cluster_pipeline.fit(X)
    song_cluster_labels = song_cluster_pipeline.predict(X)
    music_df['cluster_label'] = song_cluster_labels

    # Mesclar os dados do usuário com o DataFrame de músicas
    combined_data = pd.merge(recently_played_df[['id']], music_df, on='id', how='inner')

    # Recomendar músicas
    unheard_music = music_df[~music_df['id'].isin(combined_data['id'])]
    unheard_music_features = unheard_music[music_features]
    heard_music_features = combined_data[music_features]

    recommendation_music = get_top_recommendations(unheard_music_features, heard_music_features, unheard_music, top=10)

    recommendation_dict = recommendation_music.to_dict(orient="records")

    for rec in recommendation_dict:
        rec['track_data'] = get_track_info(rec['id'])
    
    return jsonify(recommendation_dict)