from flask import Blueprint, render_template, session, request, redirect, url_for
import podcast.episodes.services as services
import podcast.adapters.repository as repo
from podcast.episodes.services import get_podcasts, get_episodes
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
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

    max_pages = (count // 10)

    podcast = list_of_podcasts[podcast_id]

    list_of_episodes = services.sorted_episodes_by_date(repo.repository, podcast_id)

    new_review = reviewForm()

    if new_review.validate_on_submit():
        services.add_review(podcast_id, new_review.comment.data, new_review.rating.data, session['user_name'],
                            repo.repository)
        return redirect(url_for('episode_bp.episodes', podcast_id=podcast_id))

    add_to_playlist = playlistForm()
    if add_to_playlist.validate_on_submit():
        if add_to_playlist.episode_id.data is not None:
            episode_id = add_to_playlist.episode_id.data
            services.playlist_add_episode(repo.repository, 0, episode_id)

    return render_template('main.html', content_right='episodes.html', podcast=podcast, podcast_id=podcast_id,
                           episodes=list_of_episodes, max_page=max_pages,
                           reviews=reviews, average=average, new_review=new_review, add_to_playlist=add_to_playlist)


class reviewForm(FlaskForm):
    rating = IntegerField('rating')
    comment = StringField('comment', [
        DataRequired(message='Username cannot be empty')], render_kw={"class": 'test'})
    submit = SubmitField('submit')


class playlistForm(FlaskForm):
    episode_id = IntegerField('episode_id')
    submit = SubmitField('+')
