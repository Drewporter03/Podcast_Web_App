from flask import Blueprint, render_template

subscriptions_bp = Blueprint('subscriptions_bp', __name__)

@subscriptions_bp.route('/subscriptions')
def subscriptions():
        return render_template('subscriptions.html')