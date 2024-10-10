import pytest
from podcast.domainmodel.model import Podcast, Episode, Category, Playlist, PodcastSubscription, User
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

