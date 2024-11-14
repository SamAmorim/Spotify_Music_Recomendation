from flask import Blueprint, request, session, redirect, url_for
from services.auth import get_user_callback_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    
    print(code, state, session['state'])

    if not code or not state or state != session['state']:
        session['state'] = None
        session['user'] = None
        session['access_token'] = None
        return 'Código ou estado inválidos'
    
    auth_success = get_user_callback_token(code)

    if not auth_success:
        session['state'] = None
        session['user'] = None
        session['access_token'] = None
        return 'Erro na autenticação'
    
    return redirect(url_for('home'))

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()

    return redirect('/')