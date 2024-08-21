from flask import Blueprint, render_template, request
from podcast.adapters.datareader.csvdatareader import CSVDataReader
import podcast.podcasts.services as services
import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository, populate
from podcast.adapters.repository import AbstractRepository




podcasts_bp = Blueprint('podcasts_bp', __name__, template_folder='templates')


@podcasts_bp.route('/podcasts')
def podcasts():
    if request.args:
        page = int(request.args.get('page'))
        list_of_podcasts = services.sorted_podcasts_by_title(repo.repository)[page * 6 - 6: page * 6]
        if page <= 4:
            start = 1
            stop = 8
        else:
            start = page - 3
            stop = page + 4 if page + 3 < 167 else 168
            if page + 3 > 167:
                stop = 167 + 1
                start = 167 - 7
            else:
                start = page - 3
                stop = start + 7
    else:
        list_of_podcasts = services.sorted_podcasts_by_title(repo.repository)[:6]
        start, stop = 1, 8
        page = 1

    return render_template('main.html', content_right='podcasts.html', podcasts=list_of_podcasts, start = start, stop = stop, page=page)
