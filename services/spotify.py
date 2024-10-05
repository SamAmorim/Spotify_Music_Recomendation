from services.auth import get_app_access_token
from constants.spotify import SPOTIFY_BASE_URL
import requests

def get_artist_info():
    access_token = get_app_access_token()
    artist_id = '4dqkXUB9csjA7u4feEpeMF'

    artist_response = requests.get(f'{SPOTIFY_BASE_URL}/artists/{artist_id}', headers={ 'Authorization': f'Bearer {access_token}' })
    artist_response_data = artist_response.json()

    return artist_response_data
