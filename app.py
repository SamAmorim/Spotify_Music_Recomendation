# Importando a biblioteca Flask
from flask import Flask, session
from dotenv import load_dotenv
from routes import auth
from services.auth import get_user_authorize_url
from services.spotify import get_user_saved_tracks
import os

load_dotenv(verbose=True, override=True)

def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get('FLASK_SECRET_KEY')

    app.register_blueprint(auth.auth_bp)

    @app.route('/')
    def home():
        if 'access_token' not in session:
            return f'Você não está autenticado. <a href="{get_user_authorize_url()}">Faça login com o Spotify</a>'

        tracks = get_user_saved_tracks()
        return tracks
    
    return app