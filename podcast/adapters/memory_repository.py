from abc import ABC
from pathlib import Path
from datetime import date, datetime
from typing import List
from bisect import bisect, bisect_left, insort_left
from werkzeug.security import generate_password_hash
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader

class MemoryRepository(AbstractRepository, ABC):
    def __init__(self):
        self.__users = list()
        self.__add_author = list()
        self.__categories = list()
        self.__reviews = list()
        self.__podcasts = list()
        self.__episodes = list()
        self.__playlists = list()
        self.__podcast_index = dict()
        self.__episode_index = dict()
    def add_author(self, author: Author):
        insort_left(self.__add_author, author)
        self.__users.append(author)

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

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.username == username), None)

    def add_category(self, category: Category):
        self.__categories.append(category)

    def get_category(self):
        return self.__categories

    def add_review(self, review: Review):
        super().add_review(review)
        self.__reviews.append(review)

    def get_review(self):
        return self.__reviews



def load_podcasts(data_path: Path, repo: MemoryRepository):
    csv_data = CSVDataReader()
    csv_podcast = csv_data.podcasts

    for row in csv_podcast:
        podcast = Podcast(
            id=row[0],
            author=row[1],
            title=row[2],
            image=row[3],
            description=row[4],
            website=row[5],
            itunes_id=row[6],
            language=row[7],
        )
        repo.add_podcast(podcast)

def load_author(data_path: Path, repo: MemoryRepository):
    csv_data = CSVDataReader()
    csv_podcast = csv_data.podcasts
    for row in csv_podcast:
        author = Author(
            id=row[0],
            name=row[1],
        )

        repo.add_author(author)


def load_users(data_path: Path, repo: MemoryRepository):
    csv_data = CSVDataReader()
    csv_podcast = csv_data.podcasts

    for row in csv_podcast:
        podcast = Podcast(
            id = row[0],
            author=row[1],
            title=row[2],
            image=row[3],
            description=row[4],
            website=row[5],
            itunes_id=row[6],
            language=row[7],
        )
        repo.add_podcast(podcast)




