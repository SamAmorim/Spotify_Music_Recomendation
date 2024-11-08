from flask import Blueprint, render_template
from services.spotify import get_recently_played

prediction_bp = Blueprint('prediction', __name__, url_prefix='/prediction')

@prediction_bp.route('/')
def list():
    
    recently_played = get_recently_played()

    return render_template('prediction.html', recently_played=recently_played)