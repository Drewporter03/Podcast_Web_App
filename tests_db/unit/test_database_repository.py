import pytest
from podcast.domainmodel.model import Podcast, Episode, Category, Playlist, PodcastSubscription, User, Author, Review
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

# Test case to check number of eps for a specific podcast
def test_get_number_of_episodes_for_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_episodes_for_podcast(1)) == 10

# Test case to get eps for specific podcast
def test_get_episodes_for_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    episodes = repo.get_episodes_for_podcast(1)
    assert len(episodes) == 10
    assert episodes[1].title == 'Say It! Radio'

# Testing adding and getting category
def test_add_get_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    category = Category(1, "Comedy")
    repo.add_category(category)
    category2 = repo.get_category()
    assert category2[0] == category

# Testing adding multiple category
def test_adding_multiple_categories(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    category = Category(70, "Hawk")
    category_list = [category]

    repo.add_multiple_categories(category_list)
    category2 = repo.get_category()
    assert category2[67] == category_list[0]


# Code test for adding and getting reviews
def test_adding_and_getting_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    author = Author(7000, "Kumanan")
    user = User(1, "Kumanan", "Password")
    podcast = Podcast(1002, author, "HKT", "", "dammdaniel", "", "", "English")
    review = Review(1, user, podcast, 2, "sucks")
    repo.add_review(review)
    review2 = repo.get_review(1002)
    assert review2[0] == review

# Code test for searching podcast by title
def test_search_podcast_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    author = Author(7000, "Kumanan")
    podcast = Podcast(1002, author, "HKT", "", "dammdaniel", "", "", "English")
    repo.add_podcast(podcast)
    podcast2 = repo.search_podcast_by_title("HKT")
    assert podcast2[0] == podcast

# Code test for searching podcast by author
def test_search_podcast_by_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    author = Author(7000, "Kumanan")
    podcast = Podcast(1002, author, "HKT", "", "dammdaniel", "", "", "English")
    repo.add_podcast(podcast)
    podcast2 = repo.search_podcast_by_author("Kumanan")
    assert podcast2[0] == podcast

# Code test for searching podcast by categories
def test_search_podcast_by_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcast = repo.get_podcast(1)
    podcast2 =repo.search_podcast_by_category("Society & Culture")
    assert podcast2[0] == podcast