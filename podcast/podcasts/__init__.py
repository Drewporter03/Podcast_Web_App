from flask import Blueprint, render_template

podcasts_bp = Blueprint('podcasts_bp', __name__, template_folder='templates')

@podcasts_bp.route('/podcasts')
def podcasts():
        return render_template('main.html', content_right = 'podcasts.html')