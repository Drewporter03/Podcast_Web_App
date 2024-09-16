from flask import Blueprint, render_template, session
import podcast.playlists.services as services
import podcast.adapters.repository as repo

playlists_bp = Blueprint('playlists_bp', __name__, template_folder='templates')

"""TEST PLAYLIST"""
# Adding a playlist
user_playlist = services.add_playlist(repo.repository, 'bob', "My Playlist")


@playlists_bp.route('/playlists')
def playlists():
    return render_template('main.html', content_right='playlists.html', playlists=user_playlist)
