"""Initialize Flask app."""
from flask import Flask, render_template, redirect
from podcast.domainmodel.model import Podcast, Episode, Author, Category
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from pathlib import Path
import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository


from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from podcast.adapters import memory_repository, database_repository, repo_populate
from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.adapters.repo_populate import populate
from podcast.adapters.orm import mapper_registry, map_model_to_tables

def create_app(test_config=None):
    global playlists
    app = Flask(__name__)

    # configuring the app using the configuration-file settings
    app.config.from_object('config.Config')
    data_path = Path('podcasts') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repository = memory_repository.MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        repo_populate.populate(data_path, repo.repository, database_mode)

    elif app.config['REPOSITORY'] == 'database':

        database_uri = 'sqlite:///podcasts.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        app.config['SQLALCHEMY_ECHO'] = True  # echo SQL statements - useful for debugging


        # Create a database engine and connect it to the specified database
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=False)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repository = SqlAlchemyRepository(session_factory)
        data_path = Path('adapters') / 'data'




        if len(inspect(database_engine).get_table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            # Conditionally create database tables.
            mapper_registry.metadata.create_all(database_engine)
            # Remove any data from the tables.
            for table in reversed(mapper_registry.metadata.sorted_tables):
                with database_engine.connect() as conn:
                    conn.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            populate(data_path, repo.repository)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

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
    # print(repo.repository.get_episode(3))
    # print(repo.repository.get_playlist(5732178328516120769).episodes)
    # repo.repository.get_playlist(5732178328516120769).add_episode(repo.repository.get_episode(3))
    # print(repo.repository.get_playlist(5732178328516120769).episodes)
    return app
