from flask import Blueprint, render_template

prediction_bp = Blueprint('prediction', __name__, url_prefix='/prediction')

@prediction_bp.route('/')
def get():
    return render_template('prediction.html')