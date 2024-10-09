import pytest
from sqlalchemy.exc import IntegrityError
from podcast.domainmodel.model import Podcast, Review, User, Playlist, Episode, Category, Author
from sqlalchemy import text


# Testing code to insert users into database
def insert_user(empty_session, name=None, password=None):
    new_name = "Kumanan"
    new_password = "Kumanan1"

    if name is not None:
        new_name = name
    if password is not None:
        new_password = password

    empty_session.execute(
        text('INSERT INTO users (id, username, password) VALUES (:id, :username, :password)'),
        {'id': 1, 'username': new_name, 'password': new_password}
    )
    row = empty_session.execute(
        text('SELECT id from users where username = :username'),
        {'username': new_name}
    ).fetchone()
    return row[0]


def insert_podcast(empty_session):
    empty_session.execute(
        text('INSERT INTO podcasts (podcast_id, title, description, language, author_id) VALUES (:podcast_id, :title, :description, :language, :author_id)'),
        {'podcast_id': 1, 'title': "HawkTuah", 'description': "TalkTuahMe", 'language': "English", 'author_id': 2}
    )
    row = empty_session.execute(text('SELECT podcast_id from podcasts')).fetchone()
    return row[0]

# Testing code to retrieve users from to the database
def test_loading_users(empty_session):
    insert_user(empty_session, "Kumanan", "Password")
    assert empty_session.query(User).all() == [User(1, "Kumanan", "Password")]

# Test case too see if users can be saved properly to the database
def test_saving_users(empty_session):
    user = User(1, "Kumanan", "Password")
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT username, password FROM users')))
    assert rows == [("Kumanan", "Password")]

# Test case too see podcast can be loaded properly from the database
def test_loading_podcast(empty_session):
    podcast_id = insert_podcast(empty_session)
    podcast = empty_session.query(Podcast).one()

    assert podcast_id == podcast.id
    assert podcast.title == "HawkTuah"
    assert podcast.description == "TalkTuahMe"
    assert podcast.language == "English"
    assert podcast.author_id == 2

# Test case to check if podcasts are being saved properly
def test_saving_podcast(empty_session):
    author = Author(1, "Kumanan")
    podcast = Podcast(1, author, "HKT", "", "dammdaniel", "", "", "English")
    empty_session.add(podcast)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT podcast_id, title, description, language, author_id FROM podcasts')))
    assert rows ==  [(1, 'HKT', 'dammdaniel', 'English', 1)]
