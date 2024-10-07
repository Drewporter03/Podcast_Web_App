from flask import Blueprint, render_template, session, request, redirect, url_for
import podcast.episodes.services as services
import podcast.adapters.repository as repo
from podcast.episodes.services import get_podcasts
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired
from podcast.authentication.authentication import login_required
review_bp = Blueprint('review_bp', __name__, template_folder='templates')


@review_bp.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    list_of_podcasts = get_podcasts(repo.repository)

    podcast_id = request.args.get('podcast_id', type=int)
    list_of_episodes = services.get_episodes(repo.repository, podcast_id)
    average = services.get_average_reviews(podcast_id, repo.repository)

    podcast = repo.repository.get_podcast(podcast_id)

    new_review = reviewForm()

    if new_review.validate_on_submit():
        services.add_review(podcast_id, new_review.comment.data, int(new_review.rating.data), session['user_name'], repo.repository)
        return redirect(url_for('episode_bp.episodes', podcast_id = podcast_id))

    return render_template('main.html', content_right='review.html', podcast=podcast, podcast_id=podcast_id,
                           episodes=list_of_episodes, average=average, new_review=new_review)
    

class reviewForm(FlaskForm):
    rating = RadioField('Rating', choices=[(0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10')])
    comment = TextAreaField('comment', [
        DataRequired(message='Username cannot be empty')], render_kw={"class": 'test'})
    submit = SubmitField('Submit')
