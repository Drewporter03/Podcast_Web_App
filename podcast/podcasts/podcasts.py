from flask import Blueprint, render_template
from podcast.adapters.datareader.csvdatareader import CSVDataReader
import podcast.podcasts.services as services
import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository, populate
from podcast.adapters.repository import AbstractRepository




podcasts_bp = Blueprint('podcasts_bp', __name__, template_folder='templates')


@podcasts_bp.route('/podcasts')
def podcasts():
    list_of_podcasts = services.get_podcasts(repo.repository)
    return render_template('main.html', content_right='podcasts.html', podcasts=list_of_podcasts)
