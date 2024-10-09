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
        print("playlist added", playlist)

    def get_playlist(self, playlist_id: int) -> Playlist:
        for playlist in self.__playlists:
            if playlist.id == playlist_id:
                return playlist

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
        if podcast in self.__podcasts:
            self.__podcast_index[podcast.id] = podcast

    def add_ep_to_playlist(self, playlist_id, episode_id):
        pass

    def remove_ep_from_playlist(self, playlist_id, episode_id):
        pass

    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            podcast = self.__podcast_index[podcast_id]
        except KeyError:
            podcast = None

        return podcast

    def get_podcasts(self):
        # NEEDS TO BE FIXED NOT SURE WHAT IT REALLY DOES
        return self.__podcasts

    def get_number_of_podcasts(self):
        return len(self.__podcasts)

    def get_episodes(self):
        return self.__episodes

    def get_number_of_episodes(self):
        return len(self.__episodes)

    def get_episodes_for_podcast(self, podcast_id: int):
        podcast_episodes = []
        episodes = self.get_episodes()
        for episode in episodes:
            if episode.podcast.id == podcast_id:
                podcast_episodes.append(episode)
        return podcast_episodes

    def get_number_of_episodes_for_podcast(self, podcast_id: int):
        return len(self.get_episodes_for_podcast(podcast_id))

    def add_episode(self, episode: Episode):
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

    def search_podcast_by_author(self, search: str):
        podcasts = self.get_podcasts()
        search_podcasts = []
        for podcast in podcasts:
            if podcast.author.name.lower() == search.lower():
                search_podcasts.append(podcast)
        return search_podcasts

    def search_podcast_by_category(self, search: str):
        podcasts = self.get_podcasts()
        search_podcasts = []
        for podcast in podcasts:
            for category in podcast.categories:
                print(category)
                if category.name.lower() == search.lower():
                    search_podcasts.append(podcast)
        return search_podcasts

    def search_podcast_by_title(self, search: str):
        podcasts = self.get_podcasts()
        search_podcasts = []
        for podcast in podcasts:
            if podcast.title.lower() == search.lower().strip():
                search_podcasts.append(podcast)
        return search_podcasts


    def add_multiple_podcasts(self, podcasts: List[Podcast]):
        for podcast in podcasts:
            self.add_podcast(podcast)

    def add_multiple_authors(self, authors: List[Author]):
        for author in authors:
            self.add_author(author)

    def add_multiple_categories(self, categories: List[Category]):
        for category in categories:
            self.add_category(category)

    def add_multiple_episodes(self, episode: List[Episode]):
        for episode in episode:
            self.add_episode(episode)

