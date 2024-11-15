from flask import Blueprint, render_template, session, redirect
from services.report import get_most_listened_artists, get_most_listened_genres

report_bp = Blueprint('report', __name__, url_prefix='/report')

@report_bp.route('/', methods=['GET'])
def main():
    if 'user' not in session:
        return redirect('/')
    return render_template('report.html')

@report_bp.route('/most-listened-artists', methods=['GET'])
def most_listened_artists():
    return get_most_listened_artists()

@report_bp.route('/most-listened-genres', methods=['GET'])
def most_listened_genres():
    return get_most_listened_genres()