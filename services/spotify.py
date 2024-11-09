from flask import session
from constants.spotify import SPOTIFY_BASE_URL
import requests

def get_user_saved_tracks():
    url = f'{SPOTIFY_BASE_URL}/me/tracks'

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    response = requests.get(url, headers=headers)
    return response.json()

    #return map(lambda track: f'{track['track']['name']} - {track['track']['artists'][0]['name']} <br>', response.json()['items'])

# Função para obter as músicas recentemente ouvidas pelo usuário
def get_recently_played():
    url = f'{SPOTIFY_BASE_URL}/me/player/recently-played/?limit=50'

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    # Obter as músicas recentemente tocadas
    response = requests.get(url, headers=headers)
    results = response.json()

    # Concatenar as informações das músicas e features de áudio
    for item in results['items']:
        track_data = get_track_info(item['track']['id'])
        audio_features = get_audio_features(item['track']['id'])

        # Verificar se track_data e audio_features são válidos
        if track_data and audio_features:
            item['track']['track_data'] = track_data
            item['track']['audio_features'] = audio_features

    return results

def get_track_info(track_id):
    url = f'{SPOTIFY_BASE_URL}/tracks/{track_id}'

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    response = requests.get(url, headers=headers)
    return response.json()

def get_audio_features(track_id):
    url = f'{SPOTIFY_BASE_URL}/audio-features/{track_id}'

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    response = requests.get(url, headers=headers)
    return response.json()