"""Initialize Flask app."""
from flask import Flask, render_template, redirect
from podcast.domainmodel.model import Podcast, Episode, Author, Category
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.home import home_bp
from podcast.podcasts import podcasts_bp
from podcast.settings import settings_bp
from podcast.subscriptions import subscriptions_bp

# TODO: Access to the podcast should be imp``lemented via the repository pattern and using blueprints, so this can not
#  stay here!
def create_some_podcast():
    some_author = Author(1, "TED")
    some_podcast = Podcast(66, some_author, "TED Talks Daily")
    some_podcast.description = "Want TED Talks on the go? Every weekday, this feed brings you our latest talks in audio format. Hear thought-provoking ideas on every subject imaginable -- from Artificial Intelligence to Zoology, and everything in between -- given by the world's leading thinkers and doers. This collection of talks, given at TED and TEDx conferences around the globe, is also available in video format."
    some_podcast.image_url = "http://is4.mzstatic.com/image/thumb/Music128/v4/d5/c6/50/d5c65035-505e-b006-48e5-be3f0f8f19f8/source/600x600bb.jpg"
    return some_podcast


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.register_blueprint(podcasts_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(subscriptions_bp)

    @app.route('/')
    def redirect_internal():
        # Use Jinja to customize a predefined html page rendering the layout for showing a single podcast.
        return redirect("/home")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
