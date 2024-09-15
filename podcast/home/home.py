from flask import Blueprint, render_template
import podcast.adapters.repository as repo
import podcast.podcasts.services as services

home_bp = Blueprint('home_bp', __name__, template_folder='templates')


@home_bp.route('/home')
def home():
    list_of_podcasts = services.sorted_podcasts_by_title(repo.repository)


    return render_template('main.html', content_right = "home.html", podcasts=list_of_podcasts)