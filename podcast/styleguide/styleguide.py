from flask import Blueprint, render_template

styleguide_bp = Blueprint('styleguide_bp', __name__, template_folder='templates')


@styleguide_bp.route('/styleguide')
def styleguide():
    return render_template('main.html', content_right = "styleguide.html")
