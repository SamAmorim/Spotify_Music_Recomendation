import pandas as pd

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