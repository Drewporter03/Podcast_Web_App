import pytest
import datetime
from podcast.episodes import services as episode_services
from podcast.podcasts import services as podcasts_services
from podcast.domainmodel.model import Podcast, Episode, Author, Category
from podcast.episodes import services as episodes_services
from podcast.authentication import services as auth_services
from podcast.playlists import services as playlists_services
# Tests to check the retrieval of podcasts from episodes service layer
def test_get_podcast(in_memory_repo):
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")

    in_memory_repo.add_podcast(podcast1)
    list_of_podcast = episode_services.get_podcasts(in_memory_repo)

    assert podcast1 in list_of_podcast

# Tests to check the retrieval of episodes from episodes service layer
def test_get_episodes(in_memory_repo):
    author1 = Author(1, "Joe Toste")
    podcast1 = Podcast(1, author1, "Joe Toste Podcast - Sales Training Expert")
    episode1 = Episode(1, 1, "Ep1", "www.mywebsite.com", 100, "2005-09-02", "once upon a time..", podcast1)
    episode2 = Episode(2, 2, "Ep1", "www.mywebsite.com", 100, "2005-09-02", "once upon a time..", podcast1)
    episode3 = Episode(3, 3, "Ep1", "www.mywebsite.com", 100, "2005-09-02", "once upon a time..", podcast1)

    in_memory_repo.add_podcast(podcast1)
    in_memory_repo.add_episode(episode1)
    in_memory_repo.add_episode(episode2)
    in_memory_repo.add_episode(episode3)

    list_of_episodes = episode_services.get_episodes(in_memory_repo, 1)
    assert episode1 in list_of_episodes


# Tests to check if adding reviews works as intended from episodes service layer
def test_add(in_memory_repo):
    auth_services.add_user("Kumanan", "NotAGoodPassword1", in_memory_repo)
    episodes_services.add_review(2, "This podcast is good!", 6, "Kumanan", in_memory_repo)
    reviews = episodes_services.get_podcast_reviews(2, in_memory_repo)
    assert reviews[0].rating == 6
    assert reviews[0].comment == "This podcast is good!"
    assert reviews[0].reviewer.username == "Kumanan"

# Tests to check if getting the podcast reviews works as intended from episodes service layer
def test_get_podcast_review(in_memory_repo):
    auth_services.add_user("Kumanan", "NotAGoodPassword1", in_memory_repo)
    episodes_services.add_review(2, "This podcast is good!", 7, "Kumanan", in_memory_repo)
    episodes_services.add_review(2, "This podcast is not good!", 3, "Kumanan", in_memory_repo)
    episodes_services.add_review(2, "This podcast is alright", 5, "Kumanan", in_memory_repo)
    episodes_services.add_review(2, "whatever you do please dont watch this podcast, i beg of you", 0, "Kumanan", in_memory_repo)
    reviews = episodes_services.get_podcast_reviews(2, in_memory_repo)

    #Podcast 1
    assert reviews[0].rating == 7
    assert reviews[0].comment == "This podcast is good!"
    assert reviews[0].reviewer.username == "Kumanan"
    #Podcast 2
    assert reviews[1].rating == 3
    assert reviews[1].comment == "This podcast is not good!"
    assert reviews[1].reviewer.username == "Kumanan"
    #Podcast 3
    assert reviews[2].rating == 5
    assert reviews[2].comment == "This podcast is alright"
    assert reviews[2].reviewer.username == "Kumanan"
    #Podcast 4
    assert reviews[3].rating == 0
    assert reviews[3].comment == "whatever you do please dont watch this podcast, i beg of you"
    assert reviews[3].reviewer.username == "Kumanan"

# Tests to check if getting the average reviews works as intended from episode service layer
def test_get_average_review(in_memory_repo):
    auth_services.add_user("Kumanan", "NotAGoodPassword1", in_memory_repo)
    episodes_services.add_review(2, "This podcast is good!", 7, "Kumanan", in_memory_repo)
    episodes_services.add_review(2, "This podcast is not good!", 3, "Kumanan", in_memory_repo)
    episodes_services.add_review(2, "This podcast is alright", 5, "Kumanan", in_memory_repo)
    episodes_services.add_review(2, "whatever you do please dont watch this podcast, i beg of you", 0, "Kumanan",
                                 in_memory_repo)
    average_rating = episodes_services.get_average_reviews(2, in_memory_repo)

    assert average_rating == 3.8

# Tests the service function add_playlist from playlist service layer works as intended
def test_add_playlist(in_memory_repo):
    auth_services.add_user("Kumanan", "NotAGoodPassword1", in_memory_repo)
    playlist = playlists_services.add_playlist(in_memory_repo, "Kumanan", "Kumanan's Playlist")
    assert playlist.owner.username == "Kumanan"
    assert playlist.title == "Kumanan's Playlist"


# Tests the service function get_playlist from playlist service layer works as intended
def test_get_playlist(in_memory_repo):
    auth_services.add_user("Kumanan", "NotAGoodPassword1", in_memory_repo)
    playlists_services.add_playlist(in_memory_repo, "Kumanan", "Kumanan's Playlist")
    playlists = playlists_services.get_user_playlist(in_memory_repo, 0)

    assert playlists.owner.username == "Kumanan"
    assert playlists.title == "Kumanan's Playlist"


# Tests the service function add_episode from playlist service layer works as intended
def test_to_add_episode(in_memory_repo):
    auth_services.add_user("Kumanan", "NotAGoodPassword1", in_memory_repo)
    playlists_services.add_playlist(in_memory_repo, "Kumanan", "Kumanan's Playlist")
    playlists_services.add_episode(in_memory_repo, 0, 1)
    playlists = playlists_services.get_user_playlist(in_memory_repo, 0)
    assert playlists.podcast_list[0].title == "The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3"

# Tests the service function add_podcast from playlist service layer works as intended
def test_to_add_podcast(in_memory_repo):
    auth_services.add_user("Kumanan", "NotAGoodPassword1", in_memory_repo)
    playlists_services.add_playlist(in_memory_repo, "Kumanan", "Kumanan's Playlist")
    playlists_services.add_podcast(in_memory_repo, 0, 404)
    playlists = playlists_services.get_user_playlist(in_memory_repo, 0)
    assert playlists.podcast_list[0].title == "Caller Of The Week Part 2."
    assert playlists.podcast_list[1].title == "Caller Of The Week Part 1."
    assert playlists.podcast_list[3].title == "Football Picks."

# Tests the service function remove_episode from playlist service layer works as intended
def test_to_remove_episode(in_memory_repo):
    auth_services.add_user("Kumanan", "NotAGoodPassword1", in_memory_repo)
    playlists_services.add_playlist(in_memory_repo, "Kumanan", "Kumanan's Playlist")
    playlists_services.add_episode(in_memory_repo, 0, 1)
    playlists_services.remove_episode(in_memory_repo, 0, 1)
    playlists = playlists_services.get_user_playlist(in_memory_repo, 0)
    assert playlists.podcast_list == []

# Tests to check service function add_user from authentication service layer works as intended
def test_to_add_user(in_memory_repo):
    auth_services.add_user("Kumanan", "NotAGoodPassword1", in_memory_repo)
    assert  in_memory_repo.get_user("Kumanan").username == "Kumanan"


# Tests to check service function add_user from authentication service layer works as intended
def test_to_get_user(in_memory_repo):
    auth_services.add_user("Kumanan", "NotAGoodPassword1", in_memory_repo)
    user = auth_services.get_user("Kumanan", in_memory_repo)
    assert user.username == "Kumanan"

# Tests to check service function auth_user from authentication service layer works as intended
def test_to_authenticate_user(in_memory_repo):
    with pytest.raises(Exception) as auth_error:
        auth = auth_services.authenticate_user("Kumanan", "NotAGoodPassword1", in_memory_repo)
        assert str(auth_error.value) == "AuthenticationException"