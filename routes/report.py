from flask import Blueprint, render_template, session, redirect
from services.report import get_most_listened_artists, get_most_listened_genres, get_most_present_features, get_metrics, get_most_listened_hour_of_day, get_most_listened_genres_by_hour_of_day, get_most_present_words_in_title
from services.spotify import get_recently_played, get_artist_info

report_bp = Blueprint('report', __name__, url_prefix='/report')

@report_bp.route('/', methods=['GET'])
def main():
    if 'user' not in session:
        return redirect('/')
    return render_template('report.html')

@report_bp.route('/data', methods=['GET'])
def data():
    recently_played = get_recently_played()

    most_listened_artists = get_most_listened_artists(recent_tracks=recently_played)
    most_present_features = get_most_present_features(recent_tracks=recently_played)
    most_listened_hour_of_day = get_most_listened_hour_of_day(recent_tracks=recently_played)
    most_present_words = get_most_present_words_in_title(recent_tracks=recently_played)

    for track in recently_played['items']:
        for artist in track['track']['artists']:
            artist_id = artist['id']
            artist['info'] = get_artist_info(artist_id)

    most_listened_genres = get_most_listened_genres(recent_tracks=recently_played)
    genres_by_hour_of_day = get_most_listened_genres_by_hour_of_day(recent_tracks=recently_played)
    metrics = get_metrics(recent_tracks=recently_played)
    
    return {
        'most_listened_artists': most_listened_artists,
        'most_listened_genres': most_listened_genres,
        'genres_by_hour_of_day': genres_by_hour_of_day,
        'most_listened_hour_of_day': most_listened_hour_of_day,
        'most_present_words': most_present_words,
        'most_present_features': most_present_features,
        'metrics': metrics,
    }