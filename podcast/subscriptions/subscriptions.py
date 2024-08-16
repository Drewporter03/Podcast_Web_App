from flask import Blueprint, render_template

subscriptions_bp = Blueprint('subscriptions_bp', __name__, template_folder='templates')


@subscriptions_bp.route('/subscriptions')
def subscriptions():
    return render_template('main.html', content_right = 'subscriptions.html')
