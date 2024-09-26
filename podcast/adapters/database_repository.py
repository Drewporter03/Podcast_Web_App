from abc import ABC
from typing import List, Type
from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist
from sqlalchemy.orm.exc import NoResultFound


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository, ABC):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_playlist(self, playlist: Playlist):
        with self._session_cm.session() as scm:
            scm.session.merge(playlist)
            scm.commit()

    def get_playlist(self, playlist_id: int) -> Playlist:
        playlist = None
        try:
            query = self._session_cm.session.query(Playlist).filter(Playlist.id == playlist_id)
            playlist = query.one()
        except NoResultFound:
            print("No playlist found with id {}".format(playlist_id))
        return playlist

    def add_author(self, author: Author):
        with self._session_cm.session() as scm:
            scm.session.merge(author)
            scm.commit()

    def get_author(self, author_id: int) -> Author:
        authors = None
        try:
            query = self._session_cm.session.query(Author).filter(Author.id == author_id)
            authors = query.one()
        except NoResultFound:
            print("No author found with id {}".format(author_id))
        return authors

    def add_podcast(self, podcast: Podcast):
        with self._session_cm.session() as scm:
            scm.session.merge(podcast)
            scm.commit()

    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            query = self._session_cm.session.query(Podcast).filter(Podcast.id == podcast_id)
            podcast = query.one()
        except NoResultFound:
            print("No podcast found with id {}".format(podcast_id))
        return podcast
    def get_podcasts(self):
        podcasts = self._session_cm.session.query(Podcast).all()
        return podcasts
    def get_episodes(self):
        len_episodes = self._session_cm.session.query(Episode).count()
        return len_episodes

    def add_episode(self, episode: Episode):
        with self._session_cm.session() as scm:
            scm.session.merge(episode)
            scm.commit()


    def get_episode(self, episode_id: int) -> Episode:
        episode = None
        try:
            query = self._session_cm.session.query(Episode).filter(Episode.id == episode_id)
            episode = query.one()
        except NoResultFound:
            print("No episode found with id {}".format(episode_id))
        return episode

    def add_category(self, category: Category):
        with self._session_cm.session() as scm:
            scm.session.merge(category)
            scm.commit()

    def get_category(self):
        categories = self._session_cm.session.query(Category).all()
        return categories

    def get_user(self, username: str):
        user = None
        try:
            query = self._session_cm.session.query(User).filter(User.username == username)
            user = query.one()
        except NoResultFound:
            print("No User found with username {}".format(username))
        return user

    def add_user(self, user: User):
        with self._session_cm.session() as scm:
            scm.session.merge(user)
            scm.commit()

    def add_review(self, reviews: Review):
        with self._session_cm.session() as scm:
            scm.session.merge(reviews)
            scm.commit()
    def get_review(self, podcast_id: int):
        reviews = None
        try:
            query = self._session_cm.session.query(Review).filter(Review.id == podcast_id)
            reviews = query.all()
        except NoResultFound:
            print("No Review found with podcast id {}".format(podcast_id))
        return reviews