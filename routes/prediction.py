from flask import Blueprint, render_template
from services.prediction import get_music_recommendation

prediction_bp = Blueprint('prediction', __name__, url_prefix='/prediction')

@prediction_bp.route('/')
def get():
    return get_music_recommendation()