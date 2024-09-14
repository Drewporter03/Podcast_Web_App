from abc import ABC
from pathlib import Path
from datetime import date, datetime
from typing import List
from bisect import bisect, bisect_left, insort_left

import podcast
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader


class MemoryRepository(AbstractRepository, ABC):
    def __init__(self):
        self.__users = list()
        self.__author = list()
        self.__categories = list()
        self.__reviews = list()
        self.__podcasts = list()
        self.__episodes = list()
        self.__playlists = list()
        self.__podcast_index = dict()
        self.__episode_index = dict()
        self.__author_index = dict()

    def add_author(self, author: Author):
        insort_left(self.__author, author)
        self.__author_index[author.id] = author

    def get_author(self, author_id: int) -> Author:
        author = None
        try:
            author = self.__author_index[author_id]
        except KeyError:
            author = None

        return author

    def add_podcast(self, podcast: Podcast):
            insort_left(self.__podcasts, podcast)
            self.__podcast_index[podcast.id] = podcast

    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            podcast = self.__podcast_index[podcast_id]
        except KeyError:
            podcast = None

        return podcast

    def add_episode(self, episode: Episode, podcast: Podcast):
        insort_left(self.__episodes, episode)
        self.__episode_index[episode.id] = episode

    def get_episode(self, episode_id: int) -> Episode:
        episode = None
        try:
            episode = self.__episode_index[episode_id]

        except KeyError:
            episode = None

        return episode

    def add_category(self, category: Category):
        self.__categories.append(category)

    def get_category(self):
        return self.__categories


    def get_user(self, username: str):
        for user in self.__users:
            if user.username == username:
                return user
        return None

    def add_user(self, user: User):
        self.__users.append(user)

    def add_review(self, reviews: Review):
        super().add_reviews(reviews)
        self.__reviews.append(reviews)

    def get_review(self):
        return self.__reviews


def load_podcasts(data_path: Path, repo: MemoryRepository):
    csv_data = CSVDataReader()
    csv_podcast = csv_data.podcasts

    for podcast in csv_podcast:
        repo.add_podcast(podcast)

def load_author(data_path: Path, repo: MemoryRepository):
    csv_data = CSVDataReader()
    csv_authors = csv_data.authors
    for author in csv_authors:
        repo.add_author(author)

def load_category(data_path: Path, repo: MemoryRepository):
    csv_data = CSVDataReader()
    csv_category = csv_data.category
    for category in csv_category:
        repo.add_category(category)

def load_episode(data_path: Path, repo: MemoryRepository):
    csv_data = CSVDataReader()
    csv_episode = csv_data.episodes
    csv_podcast = csv_data.podcasts
    for episode in csv_episode:
        repo.add_episode(episode, csv_podcast[episode.podcast_id])

def populate(data_path: Path, repo: MemoryRepository):
    # load objects author to podcasts.
    load_author(data_path, repo)
    load_category(data_path, repo)
    load_episode(data_path, repo)
    load_podcasts(data_path, repo)

