from flask import Blueprint, render_template
import podcast.adapters.repository as repo
import podcast.podcasts.services as services
import random


home_bp = Blueprint('home_bp', __name__, template_folder='templates')


@home_bp.route('/home')
def home():
    list_of_podcasts = []
    for i in range(3):
        list_of_podcasts.append(repo.repository.get_podcast(random.randrange(1,len(repo.repository.get_podcasts()) - 1)))

    return render_template('main.html', content_right = "home.html", podcasts=list_of_podcasts)