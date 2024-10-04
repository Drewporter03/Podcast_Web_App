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
    user = services.get_user(repo.repository, user_name)
    user_id = user.id
    user_playlist = services.get_user_playlist(repo.repository, user_id)
    # user_playlist = services.get_user_playlist(repo.repository, user_id)
    # playlist_episodes = services.get_episodes(repo.repository, user_id)

    #whoopsie
    playlist_episodes = user_playlist._episodes

    remove_episode_from_playlist = RemoveEpisodeForm()
    if remove_episode_from_playlist.validate_on_submit():
        if remove_episode_from_playlist.episode_id.data is not None:
            services.remove_episode(repo.repository, user_id, remove_episode_from_playlist.episode_id.data)


    return render_template('main.html', content_right='playlists.html', playlist_episodes=playlist_episodes, user_name=user_name,
                           remove_episode_from_playlist=remove_episode_from_playlist)


class RemoveEpisodeForm(FlaskForm):
    episode_id = IntegerField()
    submit = SubmitField('−')


class RemovePodcastForm(FlaskForm):
    podcast_id = IntegerField()
    submit = SubmitField('−')

