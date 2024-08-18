from podcast.domainmodel.model import Podcast, Episode, Author, Category
from typing import List

import pytest


def test_repository_can_add_and_retrieve_podcast(in_memory_repo):
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")

    in_memory_repo.add_podcast(podcast1)

    assert in_memory_repo.get_podcast(2) is podcast1

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


def test_repository_can_add_and_retrieve_episode(in_memory_repo):
    author1 = Author(1, "Joe Toste")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    episode1 = Episode(1, 1, "Ep1", "www.mywebsite.com", 100, "2005-09-02", "once upon a time..", podcast1)
    episode2 = Episode(2, 2, "Ep1", "www.mywebsite.com", 100, "2005-09-02", "once upon a time..", podcast1)
    episode3 = Episode(3, 3, "Ep1", "www.mywebsite.com", 100, "2005-09-02", "once upon a time..", podcast1)

    in_memory_repo.add_episode(episode1, podcast1)
    in_memory_repo.add_episode(episode2, podcast1)
    in_memory_repo.add_episode(episode3, podcast1)

    assert in_memory_repo.get_episode(1) is episode1
    assert in_memory_repo.get_episode(2) is episode2
    assert in_memory_repo.get_episode(3) is episode3



