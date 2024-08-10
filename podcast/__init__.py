"""Initialize Flask app."""
from flask import Flask, render_template, redirect
from podcast.domainmodel.model import Podcast, Episode, Author, Category
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.home import home_bp
from podcast.podcasts import podcasts_bp
from podcast.settings import settings_bp
from podcast.subscriptions import subscriptions_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.register_blueprint(podcasts_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(subscriptions_bp)

    @app.route('/')
    def redirect_internal():
        return redirect("/home")
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('main.html', content_right = '404.html'), 404

    return app
