from flask import Blueprint, render_template, session
from podcast.authentication.authentication import login_required
import podcast.playlists.services as services
import podcast.adapters.repository as repo
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, RadioField, IntegerField

playlists_bp = Blueprint('playlists_bp', __name__, template_folder='templates')


@playlists_bp.route('/playlists', methods=['GET', 'POST'])
@login_required
def playlists():
    user_name = session['user_name']

    # create a generic user playlist
    user_playlist = services.add_playlist(repo.repository, user_name, f"{user_name}'s Playlist")

    remove_episode_from_playlist = RemoveEpisodeForm()
    if remove_episode_from_playlist.validate_on_submit():
        services.remove_episode(repo.repository, 0, remove_episode_from_playlist.episode_id.data)

    remove_podcast_from_playlist = RemovePodcastForm()
    if remove_podcast_from_playlist.validate_on_submit():
        services.remove_podcast(repo.repository, 0, remove_podcast_from_playlist.podcast_id.data)

    return render_template('main.html', content_right='playlists.html', playlists=user_playlist, user_name=user_name,
                           remove_episode_from_playlist=remove_episode_from_playlist,
                           remove_podcast_from_playlist=remove_podcast_from_playlist)


class RemoveEpisodeForm(FlaskForm):
    episode_id = IntegerField()
    submit = SubmitField('-')


class RemovePodcastForm(FlaskForm):
    podcast_id = IntegerField()
    submit = SubmitField('-')
