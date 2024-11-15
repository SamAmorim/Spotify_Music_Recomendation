import requests
from flask import session

from constants.spotify import SPOTIFY_BASE_URL

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
    result = response.json()

    return result

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

def get_artist_info(artist_id):
    url = f'{SPOTIFY_BASE_URL}/artists/{artist_id}'

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    response = requests.get(url, headers=headers)
    return response.json()