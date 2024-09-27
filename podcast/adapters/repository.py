import abc
from datetime import date

import typing_extensions

from podcast.domainmodel.model import Podcast, Episode, Author, Category, User, Review, Playlist
from pathlib import Path
from bisect import bisect_left, insort_left
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from typing import List

repository = None

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_playlist(self, playlist: Playlist):
        # Adds a playlist to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlist(self, playlist_id: int):
        # gets a playlist from the repository
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author: Author):
        # Adds an author to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_author(self, author_id: int):
        # gets an author from the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts(self):
        # returns all podcasts
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast(self, podcast_id: int):
        # returns one podcasts from the repository
        raise NotImplementedError

    @abc.abstractmethod
    def add_podcast(self, podcast: Podcast):
        # Adds a podcast to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_podcasts(self):
        # returns number of podcasts
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes(self):
        # returns all episodes
        raise NotImplementedError

    @abc.abstractmethod
    def get_episode(self, episode_id: int):
        # gets an episode from a podcast from the repository
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode(self, episode: Episode):
        # Adds an Episode to a podcasts to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_episodes(self):
        # returns number of episodes
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes_for_podcast(self, podcast_id: int):
        # gets all episodes belonging to a podcast
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_episodes_for_podcast(self, podcast_id: int):
        # returns number of episodes for a podcast
        raise NotImplementedError

    @abc.abstractmethod
    def get_category(self):
        # returns the category in repository
        raise NotImplementedError

    @abc.abstractmethod
    def add_category(self, category: Category):
        # adds a category to the repository
        raise NotImplementedError


    @abc.abstractmethod
    def get_user(self, username: str):
        # returns the user in the repository
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        # adds a user to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, reviews: Review):
        # adds a review to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def get_review(self, review_id: int):
        # returns the comments stored in the repository
        raise NotImplementedError

    @abc.abstractmethod
    def search_podcast_by_title(self, title: str):
        # returns podcasts with some search parameter
        raise NotImplementedError

    @abc.abstractmethod
    def search_podcast_by_author(self, title: str):
        # returns podcasts with some search parameter
        raise NotImplementedError

    @abc.abstractmethod
    def search_podcast_by_category(self, title: str):
        # returns podcasts with some search parameter
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_podcasts(self, podcast: List[Podcast]):
        # adds multiple podcasts to the repository of podcast
        raise NotImplementedError

    def add_multiple_authors(self, author: set[Author]):
        # adds multiple authors to the repository
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_episodes(self, episode: List[Episode]):
        # adds multiple episodes to the repository of episode
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_categories(self, categories: set[Category]):
        # adds many categories to the repository
        raise NotImplementedError