from podcast.domainmodel.model import Podcast, Episode, Author, Category
from typing import List
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters import repo_populate
import pytest
from pathlib import Path

# Create an author and podcast, and add podcast to repo, should return the podcast based on its ID
def test_repository_can_add_and_retrieve_podcast(in_memory_repo):
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")

    in_memory_repo.add_podcast(podcast1)

    assert in_memory_repo.get_podcast(2) is podcast1


# Create multiple authors and add them to repo, check that the author returned is based on author id
def test_repository_can_add_and_retrieve_author(in_memory_repo):
    author1 = Author(1, "Justin (Beiber) -- sorry forget last name")
    author2 = Author(2, "Drew Porter")
    author3 = Author(3, "Kumanan Piratheepan")

    in_memory_repo.add_author(author1)
    in_memory_repo.add_author(author2)
    in_memory_repo.add_author(author3)

    assert in_memory_repo.get_author(1) is author1
    assert in_memory_repo.get_author(2) is author2
    assert in_memory_repo.get_author(3) is author3


# Create multiple episodes, add them to repo and associate them with a podcast.
# Return value should be correct based on episode id
def test_repository_can_add_and_retrieve_episode(in_memory_repo):
    author1 = Author(1, "Joe Toste")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")

    episode1 = Episode(1, podcast1, "Ep1", "www.mywebsite.com", 100, "once upon a time..", "2005-09-02")
    episode2 = Episode(2, podcast1, "Ep1", "www.mywebsite.com", 100, "once upon a time..", "2005-09-02")
    episode3 = Episode(3, podcast1, "Ep1", "www.mywebsite.com", 100, "once upon a time..", "2005-09-02")



    in_memory_repo.add_episode(episode1)
    in_memory_repo.add_episode(episode2)
    in_memory_repo.add_episode(episode3)

    assert in_memory_repo.get_episode(1) is episode1
    assert in_memory_repo.get_episode(2) is episode2
    assert in_memory_repo.get_episode(3) is episode3


# create multiple categories and add them to repo, check if they exist in the repo.
def test_repository_can_add_and_retrieve_categories(in_memory_repo):
    category1 = Category(1, "cringe")
    category2 = Category(2, "funny")
    category3 = Category(3, "love")

    in_memory_repo.add_category(category1)
    in_memory_repo.add_category(category2)
    in_memory_repo.add_category(category3)

    categories = in_memory_repo.get_category()

    assert category1 in categories
    assert category2 in categories
    assert category3 in categories

def test_csv_reading_podcast(in_memory_repo):
    csv_reader = CSVDataReader()
    podcast_list = csv_reader.get_podcastcsv()
    assert podcast_list[0][0] == 1
    assert podcast_list[0][1] == "D-Hour Radio Network"
    assert podcast_list[0][2] == "http://is3.mzstatic.com/image/thumb/Music118/v4/b9/ed/86/b9ed8603-d94b-28c5-5f95-8b7061bf22fa/source/600x600bb.jpg"

def test_csv_reading_episodes(in_memory_repo):
    csv_reader = CSVDataReader()
    episode_list = csv_reader.get_episodecsv()
    assert episode_list[0][0] == 1
    assert episode_list[0][1] == 14
    assert episode_list[0][2] == "The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3"
    assert episode_list[0][3] == "http://archive.org/download/mandarian-orange-show-episode-74/mandarian-orange-show-episode-74.mp3"

