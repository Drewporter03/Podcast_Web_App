from flask import Blueprint, render_template

home_bp = Blueprint('home_bp', __name__, template_folder='templates')


@home_bp.route('/home')
def home():
    return render_template('main.html', content_right = "home.html")
