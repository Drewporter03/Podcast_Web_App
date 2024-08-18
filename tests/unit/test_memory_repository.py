from podcast.domainmodel.model import Podcast, Episode, Author, Category
from typing import List

import pytest


def test_repository_can_add_podcast(in_memory_repo):
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")

    in_memory_repo.add_podcast(podcast1)

    assert in_memory_repo.get_podcast(2) is podcast1

