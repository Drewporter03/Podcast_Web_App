from flask import Blueprint, render_template, request
import podcast.episodes.services as services
import podcast.adapters.repository as repo
from podcast.episodes.services import get_podcasts, get_episodes

playlists_bp = Blueprint('playlists_bp', __name__, template_folder='templates')


@playlists_bp.route('/playlists')
def playlists():
    return render_template('main.html', content_right='playlists.html')
