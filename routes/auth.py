from flask import Blueprint
from services.auth import get_user_authorize_url

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    authorize_url = get_user_authorize_url()
    return f'<a href="{authorize_url}">Login with Spotify</a>'