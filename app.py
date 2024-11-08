# Importando a biblioteca Flask
from flask import Flask, session, render_template
from dotenv import load_dotenv
from routes import auth, prediction
from services.auth import get_user_authorize_url
import os

load_dotenv(verbose=True, override=True)

def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get('FLASK_SECRET_KEY')

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(prediction.prediction_bp)

    @app.route('/')
    def home():
        return render_template('home.html')

        #if 'access_token' not in session:
            #return f'Você não está autenticado. <a href="{get_user_authorize_url()}">Faça login com o Spotify</a>'

        #tracks = get_user_saved_tracks()
        # return tracks
    
    @app.before_request
    def before_request():
        if 'login_url' not in session:
            session['login_url'] = get_user_authorize_url()
            
        return None

    return app