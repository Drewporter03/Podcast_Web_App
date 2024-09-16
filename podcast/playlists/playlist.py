from flask import Blueprint, render_template, session
from podcast.authentication.authentication import login_required
import podcast.playlists.services as services
import podcast.adapters.repository as repo

playlists_bp = Blueprint('playlists_bp', __name__, template_folder='templates')

@playlists_bp.route('/playlists')
@login_required
def playlists():
    user_name = session['user_name']

    #create a generic user playlist

    user_playlist = services.add_playlist(repo.repository, user_name, f"{user_name}'s Playlist")

    return render_template('main.html', content_right='playlists.html', playlists=user_playlist, user_name=user_name)
