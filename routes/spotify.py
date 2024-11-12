from flask import Blueprint, render_template
from services.spotify import get_recently_played

spotify_bp = Blueprint('spotify', __name__, url_prefix='/spotify')

@spotify_bp.route('/recently-played', methods=['GET'])
def recently_played():
    return get_recently_played()