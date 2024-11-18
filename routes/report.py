from flask import Blueprint, render_template, session, redirect
from services.report import get_most_listened_artists, get_most_listened_genres, get_most_present_features, get_metrics, get_features_in_saved_tracks

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

@report_bp.route('/most-present-features', methods=['GET'])
def most_present_features():
    return get_most_present_features()

@report_bp.route('/metrics', methods=['GET'])
def metrics():
    return get_metrics()

@report_bp.route('/features-by-dates', methods=['GET'])
def features_by_dates():
    return get_features_in_saved_tracks()