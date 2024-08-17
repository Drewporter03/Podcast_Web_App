from flask import Blueprint, render_template

episode_bp = Blueprint('episode_bp', __name__, template_folder='templates')


@episode_bp.route('/episode')
def home():
    return render_template('main.html', content_right = "home.html")
