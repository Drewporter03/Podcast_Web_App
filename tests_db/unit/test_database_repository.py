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
