from flask import session
from constants.spotify import SPOTIFY_BASE_URL
import requests

def get_user_saved_tracks():
    url = f'{SPOTIFY_BASE_URL}/me/tracks'

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    response = requests.get(url, headers=headers)

    return map(lambda track: f'{track['track']['name']} - {track['track']['artists'][0]['name']} <br>', response.json()['items'])