import pytest
from podcast.domainmodel.model import Podcast, Episode, Category, Playlist, PodcastSubscription, User, Author
from podcast.adapters.database_repository import SqlAlchemyRepository

# Test case to add and get user from database
def test_repository_can_add_and_get_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User(1, 'Kumanan', 'Kumanan!1')
    repo.add_user(user)
    user2 = repo.get_user('Kumanan')
    assert user2 == user

# Test case to check if retrieving non existant user worked as intended
def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('KumananisNotCool')
    assert user is None

# Test case to add and get playlist from database
def test_add_and_get_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User(1, 'Kumanan', 'Kumanan!1')
    playlist = Playlist(1, "Hawktuah", user, "",)
    repo.add_playlist(playlist)
    playlist2 = repo.get_playlist(playlist.id)
    assert playlist == playlist2

# Test case to add and get author from database
def test_add_and_get_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    author = Author(1, "Kumanan")
    repo.add_author(author)
    author2 = repo.get_author(1)
    assert author2 == author

# Test case to adding multiple authors
def test_add_and_multiple_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    author = Author(7000, "Kumanan1")
    author2 = Author(7001, "Kumanan2")
    author3 = Author(7002, "Kumanan3")
    author4 = Author(7003, "Kumanan4")
    author_list1 = [author, author2, author3, author4]
    repo.add_multiple_authors(author_list1)
    author_list2 = []
    for i in range(0, 4):
        author_list2.append(repo.get_author(7000+i))
    for j in range(len(author_list1)):
        assert author_list1[j] == author_list2[j]

# Test case to check number of eps
def test_get_number_of_episodes(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_number_of_episodes() == 5634