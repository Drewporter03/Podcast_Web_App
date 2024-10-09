import pytest
from sqlalchemy.exc import IntegrityError
from podcast.domainmodel.model import Podcast, Review, User, Playlist, Episode, Category
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

# Testing code to retrieve users from to the database
def test_loading_users(empty_session):
    insert_user(empty_session, "Andrew", "Password")
    assert empty_session.query(User).all() == [User(1, "Andrew", "Password")]
