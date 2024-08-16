"""Initialize Flask app."""
from flask import Flask, render_template, redirect
from podcast.domainmodel.model import Podcast, Episode, Author, Category
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def create_podcasts():
    podcast_reader = CSVDataReader()
    list_of_podcasts = podcast_reader.get_podcastcsv()


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from .home import home
        from .podcasts import podcasts
        from .settings import settings
        from .subscriptions import subscriptions
        app.register_blueprint(home.home_bp)
        app.register_blueprint(podcasts.podcasts_bp)
        app.register_blueprint(settings.settings_bp)
        app.register_blueprint(subscriptions.subscriptions_bp)

    @app.route('/')
    def redirect_internal():
        return redirect("/home")
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('main.html', content_right = '404.html'), 404

    return app
