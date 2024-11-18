import requests
from flask import session

from constants.spotify import SPOTIFY_BASE_URL

def get_user_saved_tracks(quantity = 50):
    url = f'{SPOTIFY_BASE_URL}/me/tracks?limit=50'

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    response = requests.get(url, headers=headers)
    result = response.json()

    items = result['items']

    while items.__len__() < quantity:
        if not result['next']:
            break

        response = requests.get(result['next'], headers=headers)
        result = response.json()

        items += result['items']

    result['items'] = items
    return result

# Função para obter as músicas recentemente ouvidas pelo usuário
def get_recently_played():
    url = f'{SPOTIFY_BASE_URL}/me/player/recently-played/?limit=50'

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    # Obter as músicas recentemente tocadas
    response = requests.get(url, headers=headers)
    return response.json()

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

def get_audio_features(track_ids=[]):
    url = f'{SPOTIFY_BASE_URL}/audio-features'

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    response = requests.get(url, headers=headers, params={"ids": ','.join(track_ids)})
    return response.json()

def get_artist_info(artist_id):
    url = f'{SPOTIFY_BASE_URL}/artists/{artist_id}'

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    response = requests.get(url, headers=headers)
    return response.json()