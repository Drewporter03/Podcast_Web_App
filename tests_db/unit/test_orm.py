import pytest
from sqlalchemy.exc import IntegrityError
from podcast.domainmodel.model import Podcast, Review, User, Playlist, Episode, Category, Author
from sqlalchemy import text


# code to insert users into database
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

# code to insert podcasts
def insert_podcast(empty_session):
    empty_session.execute(
        text('INSERT INTO podcasts (podcast_id, title, description, language, author_id) VALUES (:podcast_id, :title, :description, :language, :author_id)'),
        {'podcast_id': 1, 'title': "HawkTuah", 'description': "TalkTuahMe", 'language': "English", 'author_id': 2}
    )
    row = empty_session.execute(text('SELECT podcast_id from podcasts')).fetchone()
    return row[0]

# code to insert categories
def insert_categories(empty_session):
    empty_session.execute(
        text('INSERT INTO categories (category_id, category_name) VALUES (:category_id, :category_name)'),
        {'category_id': 1, 'category_name': 'Comedy'}
    )
    rows = list(empty_session.execute(text('SELECT category_id from categories')))
    keys = tuple(row[0] for row in rows)
    return keys

# code to insert podcast_categories association
def insert_podcast_categories_associations(empty_session, podcast_id, categories_ids):
    stmt = text('INSERT INTO podcast_categories (id, podcast_id, category_id) VALUES (:id, :podcast_id, :category_id)')
    for categories_id in categories_ids:
        empty_session.execute(stmt, {'id': 1, 'podcast_id': podcast_id, 'category_id': categories_id})

# code to insert review for podcasts
def insert_review(empty_session):
    podcast_id = insert_podcast(empty_session)
    user_id = insert_user(empty_session)


    empty_session.execute(
        text('INSERT INTO reviews (id, user_id, podcast_id, rating, comment) VALUES (:id , :user_id, :podcast_id, :rating, :comment)'),
        {'id': 1, 'user_id': user_id, 'podcast_id': podcast_id, 'rating': 10, 'comment': "On brodie what do it deserve to watch this"}
    )
    row = empty_session.execute(text('SELECT podcast_id from podcasts')).fetchone()
    return row[0]

# code to insert author
def insert_author(empty_session):
    empty_session.execute(
        text('INSERT INTO authors (author_id, name) VALUES (:author_id, :name)'),
        {'author_id': 1, 'name': "HawkTuah"}
    )
    row = empty_session.execute(text('SELECT author_id from authors')).fetchone()
    return row[0]


# Testing code to retrieve users from to the database
def test_loading_users(empty_session):
    insert_user(empty_session, "Kumanan", "Password")
    assert empty_session.query(User).all() == [User(1, "Kumanan", "Password")]

# Test case to see if users can be saved properly to the database
def test_saving_users(empty_session):
    user = User(1, "Kumanan", "Password")
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT username, password FROM users')))
    assert rows == [("Kumanan", "Password")]

# Test case to see podcast can be loaded properly from the database
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


# Test case to check if categories is being applied to the podcast properly using the podcast_categories table
def test_loading_of_podcast_category(empty_session):
    podcast_id = insert_podcast(empty_session)
    category_ids = insert_categories(empty_session)
    insert_podcast_categories_associations(empty_session, podcast_id, category_ids)

    podcast = empty_session.get(Podcast, podcast_id)
    categories = [empty_session.get(Category, key) for key in category_ids]

    for category in categories:
        assert podcast.categories == [category]

# Test case to check
def test_saving_podcast_category(empty_session):
    author = Author(1, "Kumanan")
    podcast = Podcast(1, author, "HKT", "", "dammdaniel", "", "", "English")
    category = Category(1, "Comedy")
    podcast.add_category(category)

    empty_session.add(podcast)
    empty_session.commit()
    rows = list(empty_session.execute(text('SELECT podcast_id FROM podcasts')))
    podcast_id = rows[0][0]

    rows = list(empty_session.execute(text('SELECT category_id, category_name FROM categories')))
    category_id = rows[0][0]
    assert rows[0][1] == "Comedy"

    rows = list(empty_session.execute(text('SELECT podcast_id, category_id from podcast_categories')))
    podcast_foreign_key = rows[0][0]
    category_foreign_key = rows[0][1]

    assert podcast_id == podcast_foreign_key
    assert category_id == category_foreign_key

# Test case to checking the loading of podcasts with reviews
def test_loading_of_reviewed_podcast(empty_session):
    insert_review(empty_session)
    rows = empty_session.query(Podcast).all()
    podcast = rows[0]

    for comment in podcast._Podcast_reviews:
        assert comment.id is podcast.id

# Test case to check saving reviewed podcast
def test_save_reviewed_podcast(empty_session):
    author = Author(1, "Kumanan")
    podcast = Podcast(1, author, "HKT", "", "dammdaniel", "", "", "English")
    user = User(1, "Kumanan", "Password")


    comment_text = "Some comment text."
    Review(1, user, podcast, 5,  comment_text)

    empty_session.add(podcast)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT podcast_id FROM podcasts')))
    podcast_id = rows[0][0]

    rows = list(empty_session.execute(text('SELECT id FROM users')))
    user_id = rows[0][0]

    rows = list(empty_session.execute(text('SELECT user_id, podcast_id, comment FROM reviews')))
    assert rows == [(user_id, podcast_id, comment_text)]

# Test case to load authors
def test_loading_author(empty_session):
    author_id = insert_author(empty_session)
    author = empty_session.query(Author).one()

    assert author_id == author.id
    assert author.name == "HawkTuah"