"""Initialize Flask app."""
from flask import Flask, render_template, redirect
from podcast.domainmodel.model import Podcast, Episode, Author, Category
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from pathlib import Path
import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters.repo_populate import populate


def create_app(test_config=None):
    global playlists
    app = Flask(__name__)

    # configuring the app using the configuration-file settings
    app.config.from_object('config.Config')
    file_path = Path('podcasts') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        file_path = app.config['TEST_DATA_PATH']

    # create a new instance of memory repository
    repo.repository = MemoryRepository()
    # populate the repository with data from csv
    populate(file_path, repo.repository)

    with app.app_context():
        from .episodes import episode
        from .home import home
        from .podcasts import podcasts
        from .review import review
        from .settings import settings
        from .authentication import authentication
        from .playlists import playlist
        # from .subscriptions import subscriptions
        app.register_blueprint(episode.episodes_bp)
        app.register_blueprint(home.home_bp)
        app.register_blueprint(podcasts.podcasts_bp)
        app.register_blueprint(settings.settings_bp)
        app.register_blueprint(review.review_bp)
        app.register_blueprint(authentication.authentication_bp)
        app.register_blueprint(playlist.playlists_bp)
        # app.register_blueprint(subscriptions.subscriptions_bp)

    @app.route('/')
    def redirect_internal():
        return redirect("/home")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('main.html', content_right='404.html'), 404

    return app
