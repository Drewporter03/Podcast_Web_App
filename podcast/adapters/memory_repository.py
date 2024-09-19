from abc import ABC
from pathlib import Path
from datetime import date, datetime
from typing import List
from bisect import bisect, bisect_left, insort_left
from podcast import CSVDataReader as csvreader
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

    def add_playlist(self, playlist: Playlist):
        insort_left(self.__playlists, playlist)
        self.__playlists.append(playlist)

    def get_playlist(self, playlist_id: int) -> Playlist:
        return self.__playlists[playlist_id]

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
        self.__reviews.append(reviews)

    def get_review(self, podcast_id: int):
        reviews = []
        for review in self.__reviews:
            if review.podcast.id == podcast_id:
                reviews.append(review)
        return reviews

csv = csvreader()
list_podcasts = []
list_episodes = []
set_authors = set()
set_categories = set()


def get_podcastcsv():
    file_path = Path(__file__).resolve().parents[0] / 'data' / 'podcasts.csv'
    info_list = csv.csv_read(file_path)

    podcast_list = []
    for row in info_list:
        # row[0] = id, row[1] = title, row[2] = image, row[3] = description, row[4] = language, row[5] = categories, row[6] = website, row[7] = author, row[8] = itunes_id
        podcast_list.append([int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], int(row[8])])
    return podcast_list

def get_episodecsv():
    file_path = Path(__file__).resolve().parents[0] / 'data' / 'episodes.csv'
    info_list = csv.csv_read(file_path)

    episode_list = []
    for row in info_list:
        # row[0] = id, row[1] = podcast_id, row[2] = title, row[3] = audio, row[4] = audio_length, row[5] = description, row[6] = pubdate
        episode_list.append([int(row[0]), int(row[1]), row[2], row[3], int(row[4]), row[5], row[6]])
    return episode_list



def load_objects():
    podcast_csv = get_podcastcsv()
    counter = 0

    for row in podcast_csv:
        if row[7] != "":
            temp_author = Author((counter + 1), row[7])
        else:
            temp_author = Author((counter + 1), "unknown")
        set_authors.add(temp_author)

        for author in set_authors:
            if temp_author.name == author.name:
                break

        if row[5] != "":
            temp_category = Category(counter + 1, row[5])
        else:
            temp_category = Category(counter + 1, "Unknown")
        set_categories.add(temp_category)

        for category in set_categories:
            if temp_category.name == category.name:
                temp_category = category
                break

        temp_podcast = Podcast(row[0], temp_author, row[1], row[2], row[3], row[6], row[8], row[4])
        temp_podcast.add_category(temp_category)
        list_podcasts.append(temp_podcast)

        counter += 1

    episode_csv = get_episodecsv()
    podcasts = list_podcasts

    for row in episode_csv:
        # initializing temp podcast # !!!!!!!!!!!!!!!!!!!!!!!!!!!!! NEEDS TO BE CHANGED LATER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        temp_podcast = list_podcasts[0]
        # Finds the matching podcast for the episode using __eq__
        for podcast in podcasts:
            if podcast.id == row[1]:
                temp_podcast = podcast
                break
        for i in range(len(row)):
            if isinstance(row[i], int):
                if row[i] == "":
                    row[i] = 0
            if isinstance(row[i], str):
                if row[i] == "":
                    row[i] = "Unknown"
        # row[0] = id, row[1] = podcast_id, row[2] = title, row[3] = audio, row[4] = audio_length, row[5] = description, row[6] = pubdate
        temp_episode = Episode(row[0], row[1], row[2], row[3], row[4], (row[6])[0:10], row[5], temp_podcast)
        list_episodes.append(temp_episode)


load_objects()

def load_podcasts(data_path: Path, repo: MemoryRepository):
    csv_podcast = list_podcasts

    for podcast in csv_podcast:
        repo.add_podcast(podcast)

def load_author(data_path: Path, repo: MemoryRepository):
    csv_authors = set_authors
    for author in csv_authors:
        repo.add_author(author)

def load_category(data_path: Path, repo: MemoryRepository):
    csv_category = set_categories
    for category in csv_category:
        repo.add_category(category)

def load_episode(data_path: Path, repo: MemoryRepository):
    csv_episode = list_episodes
    csv_podcast = list_podcasts
    for episode in csv_episode:
        repo.add_episode(episode, csv_podcast[episode.podcast_id])

def populate(data_path: Path, repo: MemoryRepository):
    # load objects author to podcasts.
    load_author(data_path, repo)
    load_category(data_path, repo)
    load_episode(data_path, repo)
    load_podcasts(data_path, repo)

