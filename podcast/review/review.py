from flask import Blueprint, render_template, session, request
import podcast.episodes.services as services
import podcast.adapters.repository as repo
from podcast.episodes.services import get_podcasts
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from functools import wraps
import podcast.authentication.services as auth_services

review_bp = Blueprint('review_bp', __name__, template_folder='templates')


@review_bp.route('/review', methods=['GET', 'POST'])
def review():

    podcast_id = request.args.get('podcast_id', type=int)

    new_review = reviewForm()
    if new_review.validate_on_submit():
        print(auth_services.get_user(session['user_name'], repo.repository))
        services.add_review(podcast_id, new_review.comment.data, new_review.rating.data, session['user_name'], repo.repository)
        print(repo.repository.__reviews)



    return render_template('main.html', content_right='review.html', podcast_id=podcast_id, new_review = new_review)

class reviewForm(FlaskForm):
    rating = IntegerField('rating')
    comment = StringField('comment', [
        DataRequired(message='Username cannot be empty')], render_kw={"class": 'test'})
    submit = SubmitField('submit')