import wtforms
from flask import Blueprint, render_template, session, request, redirect, url_for
import podcast.episodes.services as services
import podcast.playlists.services as playlist_services
import podcast.adapters.repository as repo
from podcast.episodes.services import get_podcasts, get_episodes
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, RadioField, IntegerField, StringField
from wtforms.validators import DataRequired, Length, ValidationError
from functools import wraps
import podcast.authentication.services as auth_services

episodes_bp = Blueprint('episode_bp', __name__, template_folder='templates')


@episodes_bp.route('/episodes', methods=['GET', 'POST'])
def episodes():
    list_of_podcasts = get_podcasts(repo.repository)
    podcast_id = request.args.get('podcast_id', type=int)
    list_of_episodes = services.sorted_episodes_by_date(repo.repository, podcast_id)
    average = services.get_average_reviews(podcast_id, repo.repository)
    reviews = services.get_podcast_reviews(podcast_id, repo.repository)

    count = 0
    for episode in list_of_episodes:
        if episode.podcast_id == podcast_id:
            count += 1

    podcast = repo.repository.get_podcast(podcast_id)

    list_of_episodes = services.sorted_episodes_by_date(repo.repository, podcast_id)

    new_review = reviewForm()

    if new_review.validate_on_submit():
        services.add_review(podcast_id, new_review.comment.data, int(new_review.rating.data), session['user_name'],
                            repo.repository)
        return redirect(url_for('episode_bp.episodes', podcast_id=podcast_id))

    playlist_form = PlaylistForm()

    if playlist_form.validate_on_submit():
        episode_id = playlist_form.episode_id.data
        action = playlist_form.action.data
        if action == "REMOVE":
            episode_id = playlist_form.episode_id.data
            playlist_services.remove_episode(repo.repository, 0, episode_id)
        elif action == "ADD":
            playlist_services.add_episode(repo.repository, 0, episode_id)

    if 'user_name' in session:
        playlist_episodes = playlist_services.get_user_playlist(repo.repository, 0).podcast_list
    else:
        playlist_episodes = None

    return render_template('main.html', content_right='episodes.html', podcast=podcast, podcast_id=podcast_id,
                           episodes=list_of_episodes,
                           reviews=reviews, average=average, new_review=new_review, playlist_form=playlist_form,
                           playlist_episodes=playlist_episodes)


class reviewForm(FlaskForm):
    rating = RadioField('Rating',
                        choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'),
                                 (8, '8'), (9, '9'), (10, '10')])
    comment = TextAreaField('comment', [
        DataRequired(message='Username cannot be empty')], render_kw={"class": 'test'})
    submit = SubmitField('submit')


class PlaylistForm(FlaskForm):
    episode_id = IntegerField('episode_id')
    action = StringField('action')
    submit = SubmitField('')
