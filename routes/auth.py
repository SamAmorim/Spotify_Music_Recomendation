from flask import Blueprint, request, session, redirect, url_for
from services.auth import get_user_authorize_url, get_user_callback_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    authorize_url = get_user_authorize_url()
    return f'<a href="{authorize_url}">Faça login com o Spotify</a>'

@auth_bp.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')

    if not code or not state or state != session['state']:
        return 'Erro na requisição'
    
    auth_success = get_user_callback_token(code)

    if not auth_success:
        return 'Erro na autenticação'
    
    return redirect(url_for('home'))