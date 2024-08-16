from flask import Blueprint, render_template, request
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def create_podcasts():
    podcast_reader = CSVDataReader()
    list_of_podcasts = podcast_reader.get_podcastcsv()
    return list_of_podcasts


podcasts_bp = Blueprint('podcasts_bp', __name__, template_folder='templates')


@podcasts_bp.route('/podcasts')
def podcasts():
    if request.args:
        page = int(request.args.get('page'))
        list_of_podcasts = create_podcasts()[page * 6 - 6: page * 6]
        start, stop = page - 3, page + 3
    else:
        list_of_podcasts = create_podcasts()[:6]
        start, stop = 1, 7

    return render_template('main.html', content_right='podcasts.html', podcasts=list_of_podcasts, start = start, stop = stop)
