from flask import Blueprint, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField

import podcast.adapters.repository as repo
import podcast.playlists
import podcast.podcasts.services as services
import podcast.playlists.services as playlist_services
import podcast.episodes.services as episodes_services


podcasts_bp = Blueprint('podcasts_bp', __name__, template_folder='templates')


@podcasts_bp.route('/podcasts', methods=['POST', 'GET'])
def podcasts():
    list_of_podcasts = services.sorted_podcasts_by_title(repo.repository)
    list_of_episodes = services.get_episodes(repo.repository)
    max_pages = services.calculate_pages(list_of_podcasts)

    if request.args:
        query = request.args.get('q')
        parameter = request.args.get('p')
        page = (request.args.get('page', default=1, type=int))

        if query is not None:
            list_of_podcasts = services.filter_podcasts(list_of_podcasts, query, parameter)
            max_pages = services.calculate_pages(list_of_podcasts)

        start, stop, list_of_podcasts = services.calculate_pagination(page, max_pages, list_of_podcasts)

    else:
        page = 1
        start, stop, list_of_podcasts = services.calculate_pagination(page, max_pages, list_of_podcasts)

    playlist_form = playlistForm()
    if playlist_form.validate_on_submit():
        podcast_id = playlist_form.podcast_id.data
        action = playlist_form.action.data

        if action == 'REMOVE':
            episodes_to_remove = [episode for episode in
                                  playlist_services.get_user_playlist(repo.repository, 0).podcast_list if
                                  episode.podcast.id == podcast_id]

            for episode in episodes_to_remove:
                playlist_services.remove_episode(repo.repository, 0, episode.id)

        elif action == 'ADD':
            playlist_services.add_podcast(repo.repository, 0, podcast_id)

    if 'user_name' in session:
        playlist_episodes = playlist_services.get_user_playlist(repo.repository, 0).podcast_list
    else:
        playlist_episodes = None
    
    status = {}
    for podcast in list_of_podcasts:
        status[podcast.id] = True
        for episode in list_of_episodes:
            if episode.podcast.id == podcast.id:
                if episode not in playlist_episodes:
                    status[podcast.id] = False


    return render_template('main.html', content_right='podcasts.html', podcasts=list_of_podcasts, start=start,
                           stop=stop, page=page, max_pages=max_pages, playlist_form=playlist_form,
                           playlist_episodes=playlist_episodes, list_of_episodes=list_of_episodes, status = status)


class playlistForm(FlaskForm):
    podcast_id = IntegerField('podcast_id')
    submit = SubmitField('')
    action = StringField('action')
