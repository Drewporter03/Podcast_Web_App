from flask import Blueprint, render_template, request
import podcast.playlists.services as services
import podcast.adapters.repository as repo

playlists_bp = Blueprint('playlists_bp', __name__, template_folder='templates')

"""TEST PLAYLIST"""
# user_playlist = services.add_playlist(repo.repository, "bob", "My Playlist")
# services.add_episode(repo.repository,0, 7)
# services.add_episode(repo.repository,0, 6)
# services.add_episode(repo.repository,0, 718)



@playlists_bp.route('/playlists')
def playlists():
    return render_template('main.html', content_right='playlists.html', playlists=user_playlist)
