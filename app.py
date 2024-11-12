from flask import Flask, session, render_template
from dotenv import load_dotenv
from routes import auth, report, spotify, prediction
from services.auth import get_user_authorize_url
import os

load_dotenv(verbose=True, override=True)

def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get('FLASK_SECRET_KEY')

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(report.report_bp)
    app.register_blueprint(spotify.spotify_bp)
    app.register_blueprint(prediction.prediction_bp)

    @app.route('/', methods=['GET'])
    def home():
        return render_template('home.html')
    
    @app.before_request
    def before_request():
        if 'login_url' not in session:
            session['login_url'] = get_user_authorize_url()
            
        return None

    return app