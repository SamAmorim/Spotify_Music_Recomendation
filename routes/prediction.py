from flask import Blueprint
from services.prediction import get_music_recommendation

prediction_bp = Blueprint('prediction', __name__, url_prefix='/prediction')

@prediction_bp.route('/', methods=['GET'])
def get():
    return get_music_recommendation()