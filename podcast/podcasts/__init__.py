from flask import Blueprint, render_template
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def create_podcasts():
    podcast_reader = CSVDataReader()
    list_of_podcasts = podcast_reader.get_podcastcsv()
    return list_of_podcasts


podcasts_bp = Blueprint('podcasts_bp', __name__, template_folder='templates')


@podcasts_bp.route('/podcasts')
def podcasts():
    list_of_podcasts = create_podcasts()
    return render_template('main.html', content_right='podcasts.html', podcasts=list_of_podcasts)
