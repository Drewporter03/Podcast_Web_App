from flask import Blueprint, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField

import podcast.adapters.repository as repo
import podcast.playlists
import podcast.podcasts.services as services
import podcast.playlists.services as playlist_services
import podcast.episodes.services as episodes_services


podcasts_bp = Blueprint('podcasts_bp', __name__, template_folder='templates')


def filter_podcasts(podcasts, query, parameter):
    searched_podcasts = []
    for podcast in podcasts:
        if parameter == "title" and query in podcast.title:
            searched_podcasts.append(podcast)
        elif parameter == "author" and query in podcast.author.name:
            searched_podcasts.append(podcast)
        elif parameter == "category" and query in podcast.categories[0].name:
            searched_podcasts.append(podcast)

    return searched_podcasts


def calculate_pagination(page, max_pages, list_of_podcasts):
    if page <= 4:
        start = 1
        stop = 8 if max_pages > 8 else max_pages + 1
    else:
        if page + 3 > max_pages:
            stop = max_pages + 1
            start = 1 if max_pages - 7 <= 1 else max_pages - 7
        else:
            start = page - 3
            stop = start + 7
    list_of_podcasts = list_of_podcasts[page * 10 - 10: page * 10]

    return start, stop, list_of_podcasts


def calculate_pages(list_of_podcasts):
    number_of_episodes = len(list_of_podcasts)
    return int(round(number_of_episodes / 10))


@podcasts_bp.route('/podcasts', methods=['POST', 'GET'])
def podcasts():
    list_of_podcasts = services.sorted_podcasts_by_title(repo.repository)
    list_of_episodes = services.get_episodes(repo.repository)
    max_pages = calculate_pages(list_of_podcasts)

    if request.args:
        query = request.args.get('q')
        parameter = request.args.get('p')
        page = (request.args.get('page', default=1, type=int))

        if query is not None:
            list_of_podcasts = filter_podcasts(list_of_podcasts, query, parameter)
            max_pages = calculate_pages(list_of_podcasts)

        start, stop, list_of_podcasts = calculate_pagination(page, max_pages, list_of_podcasts)

    else:
        page = 1
        start, stop, list_of_podcasts = calculate_pagination(page, max_pages, list_of_podcasts)

    playlist_form = playlistForm()
    if playlist_form.validate_on_submit():
        podcast_id = playlist_form.podcast_id.data
        action = playlist_form.action.data

        if action == 'REMOVE':
            episodes_to_remove = [episode for episode in
                                  playlist_services.get_user_playlist(repo.repository, 0).podcast_list if
                                  episode.podcast_id == podcast_id]

            for episode in episodes_to_remove:
                playlist_services.remove_episode(repo.repository, 0, episode.id)
                print("removed podcast", podcast_id)

        elif action == 'ADD':
            try:
                playlist_services.get_user_playlist(repo.repository, 0)
            except playlist_services.PlaylistNotFoundException:
                user_name = session['user_name']
                playlist_services.add_playlist(repo.repository, user_name, f"{user_name}'s Playlist")
            playlist_services.add_podcast(repo.repository, 0, podcast_id)
            print("added podcast", podcast_id)

    if 'user_name' in session:
        try:
            playlist_episodes = playlist_services.get_user_playlist(repo.repository, 0).podcast_list
        except playlist_services.PlaylistNotFoundException:
            user_name = session['user_name']
            playlist_services.add_playlist(repo.repository, user_name, f"{user_name}'s Playlist")
            playlist_episodes = playlist_services.get_user_playlist(repo.repository, 0).podcast_list
    else:
        playlist_episodes = None

    return render_template('main.html', content_right='podcasts.html', podcasts=list_of_podcasts, start=start,
                           stop=stop, page=page, max_pages=max_pages, playlist_form=playlist_form, playlist_episodes=playlist_episodes, list_of_episodes=list_of_episodes)


class playlistForm(FlaskForm):
    podcast_id = IntegerField('podcast_id')
    submit = SubmitField('')
    action = StringField('action')
