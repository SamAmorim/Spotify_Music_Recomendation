from services.spotify import get_recently_played, get_artist_info, get_audio_features, get_user_saved_tracks
import pandas as pd
import numpy as np

def get_most_listened_artists(recent_tracks):
    artists = {}

    for track in recent_tracks['items']:
        artist = track['track']['artists'][0]['name']
        image_url = track['track']['album']['images'][0]['url']

        if artist in artists:
            artists[artist]['count'] += 1
        else:
            artists[artist] = {'count': 1, 'image_url': image_url}

    return sorted(artists.items(), key=lambda x: x[1]['count'], reverse=True)[:10]

def get_most_listened_genres(recent_tracks):
    genres = {}

    for track in recent_tracks['items']:
        for artist in track['track']['artists']:
            for genre in artist['info']['genres']:
                if genre in genres:
                    genres[genre] += 1
                else:
                    genres[genre] = 1

    # Retornar os 10 gêneros mais ouvidos, ordenados alfabeticamente
    by_quantity = sorted(genres.items(), key=lambda x: x[1], reverse=True)[:10]
    return sorted(by_quantity, key=lambda x: x[0])

def get_most_listened_genres_by_hour_of_day(recent_tracks):
    genres = {}

    for track in recent_tracks['items']:
        played_at = track['played_at']
        hour = int(played_at.split('T')[1][:2])-3

        for artist in track['track']['artists']:
            for genre in artist['info']['genres']:
                if genre not in genres:
                    genres[genre] = [0]*24

                genres[genre][hour] += 1

    most_listened_genres = sorted(genres.items(), key=lambda x: sum(x[1]), reverse=True)[:6]
    return {genre: hours for genre, hours in most_listened_genres}

def get_most_present_words_in_title(recent_tracks):
    words = {}

    exclude = ['-', 'remaster', 'the', 'a', 'an', 'of', 'in', 'on', 'at', 'for', 'with', 'and', 'or', 'but', 'nor', 'so', 'yet', 'to', 'from', 'by', 'as',
               'o', 'um', 'uma', 'de', 'em', 'no', 'na', 'para', 'com', 'e', 'ou', 'mas', 'nem', 'por', 'como']

    for track in recent_tracks['items']:
        title = track['track']['name']
        for word in title.split(' '):
            word = word.lower()
            if word not in exclude:
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1

    return sorted(words.items(), key=lambda x: x[1], reverse=True)[:10]

def get_most_listened_hour_of_day(recent_tracks):
    hours = np.zeros(24)

    for track in recent_tracks['items']:
        played_at = track['played_at']
        hour = int(played_at.split('T')[1][:2])-3
        hours[hour] += 1

    return hours.tolist()

def get_most_present_features(recent_tracks):
    features = {
        'acousticness': 0,
        'danceability': 0,
        'energy': 0,
        'instrumentalness': 0,
        'liveness': 0,
        'speechiness': 0,
        'valence': 0
    }

    track_ids = list(map(lambda x: x['track']['id'], recent_tracks['items']))
    tracks_features = get_audio_features(track_ids)

    for track_features in tracks_features['audio_features']:
        for feature in features:
            features[feature] += track_features[feature]

    for feature in features:
        features[feature] /= len(recent_tracks['items'])

    return features

def get_metrics(recent_tracks):
    genres = []

    for track in recent_tracks['items']:
        for artist in track['track']['artists']:
            for genre in artist['info']['genres']:
                if genre not in genres:
                    genres.append(genre)

    # Normaliza o JSON recebido
    df = pd.json_normalize(recent_tracks['items'])
    genres_df = pd.DataFrame(genres, columns=['genres'])

    # Ajusta a coluna 'track.artists' para conter apenas os IDs dos artistas
    df['track.artists'] = df['track.artists'].apply(lambda x: [artist['name'] for artist in x])

    # Conta os valores únicos para as colunas relevantes
    unique_values = {
        'tracks': len(df['track.id'].unique()),       # Número de faixas únicas
        'artists': len(df['track.artists'].explode().unique()),  # Número de artistas únicos
        'albums': len(df['track.album.id'].unique()), # Número de álbuns únicos
        'genres': len(genres_df['genres'].explode().unique())
    }

    return unique_values

def get_features_in_saved_tracks():
    saved_tracks = get_user_saved_tracks(100)

    features_template = {
        'acousticness': 0,
        'danceability': 0,
        'energy': 0,
        'instrumentalness': 0,
        'liveness': 0,
        'speechiness': 0,
        'valence': 0
    }

    dates = {}

    print(len(saved_tracks['items']))

    for track in saved_tracks['items']:
        track_id = track['track']['id']
        added_at = track['added_at']
        audio_features = get_audio_features(track_id)

        if added_at not in dates:
            dates[added_at] = features_template.copy()

        for feature in features_template:
            print(feature, audio_features[feature])
            dates[added_at][feature] += audio_features[feature]

    for date in dates:
        print(date)
        for feature in features_template:
            print(dates[date][feature])
            dates[date][feature] /= len(saved_tracks['items'])
            print(dates[date][feature])

    return dates