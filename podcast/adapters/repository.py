import abc
from datetime import date
from podcast.domainmodel.model import Podcast, Episode, Author, Category, User, Review
from pathlib import Path
from bisect import bisect_left, insort_left
from podcast.adapters.datareader.csvdatareader import CSVDataReader


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_author(self, author: Author):
        # Adds a author to the repository
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
    def get_podcast_by_date(self, podcast_id: int):
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
    def add_user(self, user: User):
        # adds a user to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username):
        # gets a user from a list of usernames from the repository
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
    def add_review(self, review: Review):
        # adds a review to the repository

        if review.reviewer is None or review.reviewer == "":
            # raises error when review is not linked to reviewer
            raise Exception("EROR: Review not linked to a user")

        raise NotImplementedError

    @abc.abstractmethod
    def get_review(self):
        # returns reviews from the repository
        raise NotImplementedError


    @abc.abstractmethod
    def add_category(self, category: Category):
        # adds categories to repository
        raise NotImplementedError

    def get_category(self):
        # gets categories to repository
        raise NotImplementedError
