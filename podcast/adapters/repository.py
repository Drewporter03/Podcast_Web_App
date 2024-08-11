import abc
from datetime import date
from podcast.domainmodel.model import Podcast, Episode, Author, Category
from pathlib import Path
from bisect import bisect_left, insort_left


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_podcast(self, podcast: Podcast):
        # Adds a podcast to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast(self, podcast_id: int):
        # returns podcasts from the repository
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode(self, episode: Episode, podcast: Podcast):
        # Adds an Episode to a podcasts to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_episode(self, episode_id: int):
        # gets an episode from a podcast from the repository
        raise NotImplementedError
