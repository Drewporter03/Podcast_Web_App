import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from pathlib import Path
import podcast.adapters.repository as repo
from podcast.adapters.database_repository import SqlAlchemyRepository

from podcast.adapters import database_repository, repo_populate
from podcast.adapters.orm import mapper_registry, map_model_to_tables


TEST_DATA_PATH_DATABASE_FULL = Path(__file__).parent / 'adapters' / 'data'
TEST_DATA_PATH_DATABASE_LIMITED = Path(__file__).parent / "tests" / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///podcast-test.db'

@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    mapper_registry.metadata.create_all(engine)  # Conditionally create database tables.

    for table in reversed(mapper_registry.metadata.sorted_tables):
        with engine.connect() as conn:
            conn.execute(table.delete())


    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repo_populate.populate(TEST_DATA_PATH_DATABASE_LIMITED, repo_instance, database_mode)
    yield engine
    mapper_registry.metadata.drop_all(engine)
@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    mapper_registry.metadata.create_all(engine)

    for table in reversed(mapper_registry.metadata.sorted_tables):
        with engine.connect() as conn:
            conn.execute(table.delete())

    map_model_to_tables()

    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)

    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)

    database_mode = True
    repo_populate.populate(TEST_DATA_PATH_DATABASE_FULL, repo_instance, database_mode)
    yield session_factory
    mapper_registry.metadata.drop_all(engine)
@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    mapper_registry.metadata.create_all(engine)

    for table in reversed(mapper_registry.metadata.sorted_tables):
        with engine.connect() as conn:
            conn.execute(table.delete())

    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    mapper_registry.metadata.drop_all(engine)

