import pytest
import datetime
from podcast.episodes import services as episode_services
from podcast.podcasts import services as podcasts_services
from podcast.domainmodel.model import Podcast, Episode, Author, Category

def test_get_podcast(in_memory_repo):
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")

    in_memory_repo.add_podcast(podcast1)
    list_of_podcast = episode_services.get_podcasts(in_memory_repo)

    assert podcast1 in list_of_podcast

def test_get_episodes(in_memory_repo):
    author1 = Author(1, "Joe Toste")
    podcast1 = Podcast(1, author1, "Joe Toste Podcast - Sales Training Expert")
    episode1 = Episode(1, 1, "Ep1", "www.mywebsite.com", 100, "2005-09-02", "once upon a time..", podcast1)
    episode2 = Episode(2, 2, "Ep1", "www.mywebsite.com", 100, "2005-09-02", "once upon a time..", podcast1)
    episode3 = Episode(3, 3, "Ep1", "www.mywebsite.com", 100, "2005-09-02", "once upon a time..", podcast1)

    in_memory_repo.add_podcast(podcast1)
    in_memory_repo.add_episode(episode1, podcast1)
    in_memory_repo.add_episode(episode2, podcast1)
    in_memory_repo.add_episode(episode3, podcast1)

    list_of_episodes = episode_services.get_episodes(in_memory_repo, 1)
    assert episode1 in list_of_episodes

