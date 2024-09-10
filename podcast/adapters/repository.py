import abc
from datetime import date
from podcast.domainmodel.model import Podcast, Episode, Author, Category, User, Review
from pathlib import Path
from bisect import bisect_left, insort_left
from podcast.adapters.datareader.csvdatareader import CSVDataReader

repository = None

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_author(self, author: Author):
        # Adds a author to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_author(self, author_id: int):
        # gets a author to the repository
        raise NotImplementedError

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


    @abc.abstractmethod
    def add_category(self, category: Category):
        # adds a category to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_category(self):
        # returns the category in repository
        raise NotImplementedError


    @abc.abstractmethod
    def get_user(self, username: str):
        # returns the user in the repository
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        # adds a user to the repository
        raise NotImplementedError