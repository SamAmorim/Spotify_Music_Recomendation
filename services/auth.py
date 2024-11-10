import requests
import base64
import time
import os
from flask import session
from constants.spotify import SPOTIFY_AUTH_URL, SPOTIFY_BASE_URL

def get_user_authorize_url():
    url = f"{SPOTIFY_AUTH_URL}/authorize"

    random_state = int(time.time())
    session['state'] = f'{random_state}'

    query_params = {
        'response_type': 'code',
        'redirect_uri': os.environ.get('SPOTIFY_API_REDIRECT_URI'),
        'client_id': os.environ.get('SPOTIFY_API_CLIENT_ID'),
        'scope': 'user-read-recently-played',
        'state': random_state
    }

    response = requests.get(url, params=query_params)

    return response.url

def get_user_callback_token(code):
    url = f"{SPOTIFY_AUTH_URL}/api/token"

    query_params = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.environ.get('SPOTIFY_API_REDIRECT_URI')
    }

    client_id = os.environ.get('SPOTIFY_API_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_API_CLIENT_SECRET')

    secrets = f"{client_id}:{client_secret}".encode('ascii')
    authorization = base64.b64encode(secrets).decode('ascii')

    headers = {
        'Authorization': f'Basic {authorization}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=query_params, headers=headers)

    if response.status_code != 200:
        return False
    
    session['access_token'] = response.json()['access_token']
    session['user'] = get_user_profile()

    return True

def get_user_profile():
    url = f"{SPOTIFY_BASE_URL}/me"

    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }

    response = requests.get(url, headers=headers)

    print(response.content)

    return response.json()