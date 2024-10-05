import requests
import time
import os
from flask import session
from constants.spotify import SPOTIFY_AUTH_URL

def get_app_access_token():
    access_token = session.get('access_token')
    expires_in = session.get('expires_in')
    last_request_time = session.get('last_request_time')

    if access_token is None or time.time() - last_request_time > expires_in:
        auth_response = requests.post(f"{SPOTIFY_AUTH_URL}/api/token", data={
            'grant_type': 'client_credentials',
            'client_id': os.environ.get('SPOTIFY_API_CLIENT_ID'),
            'client_secret': os.environ.get('SPOTIFY_API_CLIENT_SECRET')
        })

        auth_response_data = auth_response.json()

        session['access_token'] = auth_response_data['access_token']
        session['expires_in'] = auth_response_data['expires_in']
        session['last_request_time'] = time.time()

    return session['access_token']

def get_user_authorize_url():
    url = f"{SPOTIFY_AUTH_URL}/authorize"
    query_params = {
        'response_type': 'code',
        'redirect_uri': os.environ.get('SPOTIFY_REDIRECT_URI'),
        'client_id': os.environ.get('SPOTIFY_API_CLIENT_ID'),
        'scope': 'user-libary-read'
    }

    response = requests.get(url, params=query_params)

    print(response)
    print(response.url)

    return response.url