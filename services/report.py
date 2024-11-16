from services.spotify import get_recently_played, get_artist_info, get_audio_features

def get_most_listened_artists():
    recent_tracks = get_recently_played()

    artists = {}

    for track in recent_tracks['items']:
        artist = track['track']['artists'][0]['name']
        image_url = track['track']['album']['images'][0]['url']

        if artist in artists:
            artists[artist]['count'] += 1
        else:
            artists[artist] = {'count': 1, 'image_url': image_url}

    return sorted(artists.items(), key=lambda x: x[1]['count'], reverse=True)[:10]

def get_most_listened_genres():
    recent_tracks = get_recently_played()

    genres = {}

    for track in recent_tracks['items']:
        artist_id = track['track']['artists'][0]['id']
        artist = get_artist_info(artist_id)
        
        print(artist)

        for genre in artist['genres']:
            if genre in genres:
                genres[genre] += 1
            else:
                genres[genre] = 1

    # Retornar os 10 gêneros mais ouvidos, ordenados alfabeticamente
    by_quantity = sorted(genres.items(), key=lambda x: x[1], reverse=True)[:10]
    return sorted(by_quantity, key=lambda x: x[0])

def get_most_present_features():
    recent_tracks = get_recently_played()

    features = {
        'acousticness': 0,
        'danceability': 0,
        'energy': 0,
        'instrumentalness': 0,
        'liveness': 0,
        'speechiness': 0,
        'valence': 0
    }

    for track in recent_tracks['items']:
        track_id = track['track']['id']
        audio_features = get_audio_features(track_id)

        for feature in features:
            features[feature] += audio_features[feature]

    for feature in features:
        features[feature] /= len(recent_tracks['items'])

    return features