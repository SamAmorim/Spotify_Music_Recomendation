# Importando a biblioteca Flask
from flask import Flask
from dotenv import load_dotenv
from routes import auth
from services.spotify import get_artist_info
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get('FLASK_SECRET_KEY')

    app.register_blueprint(auth.auth_bp)

    @app.route('/')
    def home():
        artist_info = get_artist_info()
        return artist_info
    
    return app