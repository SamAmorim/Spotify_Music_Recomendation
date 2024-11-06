from flask import Flask, jsonify, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics.pairwise import cosine_similarity

# Iniciar o app Flask
app = Flask(__name__)

# Caminhos dos arquivos de dados
music_data_path = "music_data/music_data.csv"
genre_df_path = "music_data/data_by_genres.csv"
year_data_path = "music_data/data_by_year.csv"

# Carregar os dados das músicas
music_df = pd.read_csv(music_data_path)


# Função para obter as músicas recentemente ouvidas pelo usuário
def get_read_recently_played(client_id, client_secret, redirect_uri):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope='user-read-recently-played'))
    tracks_info = []
    limit = 50

    try:
        # Obter as músicas recentemente tocadas
        results = sp.current_user_recently_played(limit=limit)

        if results['items']:
            for item in results['items']:
                track_data = sp.track(item['track']['id'])
                audio_features = sp.audio_features(item['track']['id'])[0]

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

    except Exception as e:
        print(f"Erro ao obter dados das músicas: {e}")


# Função para recomendar músicas com base nas músicas ouvidas pelo usuário
def get_top_recommendations(unheard_music_features, heard_music_features, unheard_music, top=10):
    similarities = cosine_similarity(unheard_music_features, heard_music_features)
    similarity_scores = similarities.sum(axis=1)

    unheard_music['similarity'] = similarity_scores
    top_recommendations = unheard_music.sort_values(by='similarity', ascending=False).drop_duplicates(
        subset=['id']).head(top)

    recommendation_df = top_recommendations[['name', 'artists', 'similarity']]
    return recommendation_df


# Rota para obter recomendações baseadas nas músicas ouvidas pelo usuário
@app.route('/recommend', methods=['GET'])
def recommend_music():
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')
    redirect_uri = request.args.get('redirect_uri')

    # Obter músicas recentemente ouvidas pelo usuário
    user_recent_tracks = get_read_recently_played(client_id, client_secret, redirect_uri)

    # Alinhar tipos de dados para garantir consistência ao adicionar novas músicas
    for col in music_df.columns:
        if col in user_recent_tracks.columns:
            user_recent_tracks[col] = user_recent_tracks[col].astype(music_df[col].dtype)

    # Identificar e adicionar novas músicas ao DataFrame
    new_tracks = user_recent_tracks[~user_recent_tracks['id'].isin(music_df['id'])]
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
    combined_data = pd.merge(user_recent_tracks[['id']], music_df, on='id', how='inner')

    # Recomendar músicas
    unheard_music = music_df[~music_df['id'].isin(combined_data['id'])]
    unheard_music_features = unheard_music[music_features]
    heard_music_features = combined_data[music_features]

    recommendation_music = get_top_recommendations(unheard_music_features, heard_music_features, unheard_music, top=10)

    return jsonify(recommendation_music.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
