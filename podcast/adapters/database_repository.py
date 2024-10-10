from abc import ABC
from typing import List, Type

import sqlalchemy.orm
import sqlalchemy.orm.session
from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import insert


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
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
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
        with self._session_cm as scm:
            scm.session.add(playlist)
            scm.commit()
            print(scm.session.query(Playlist).all())

    def get_playlist(self, playlist_id: int) -> Playlist:
        with self._session_cm as scm:
            playlist = scm.session.get(Playlist, playlist_id)
        return playlist

    def add_author(self, author: Author):
        with self._session_cm.session() as scm:
            scm.session.merge(author)
            scm.commit()

    def add_multiple_authors(self, authors: List[Author]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    if author.name is None:
                        raise ValueError("Author name cannot be None")
                    scm.session.add(author)
            scm.commit()


    def get_author(self, author_id: int) -> Author:
        authors = None
        try:
            author = self._session_cm.session.query(Author).get(author_id)
        except NoResultFound:
            print("No author found with id {}".format(author_id))
        return authors

    # PODCASTS REGION

    def get_podcasts(self):
        podcasts = self._session_cm.session.query(Podcast).all()
        return podcasts

    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            podcast = self._session_cm.session.query(Podcast).get(podcast_id)

        except NoResultFound:
            print("No podcast found with id {}".format(podcast_id))
        return podcast

    def add_podcast(self, podcast: Podcast):
        with self._session_cm.session() as scm:
            scm.session.merge(podcast)
            scm.commit()

    def add_multiple_podcasts(self, podcasts: List[Podcast]):
        with self._session_cm as scm:
            for podcast in podcasts:
                scm.session.add(podcast)
            scm.commit()
    def get_number_of_podcasts(self) -> int:
        num_podcasts = self._session_cm.session.query(Podcast).count()
        return num_podcasts

    # END REGION

    # EPISODES REGION
    def get_episodes(self) -> list[Type[Episode]]:
        episodes = self._session_cm.session.query(Episode).all()
        return episodes

    def get_episode(self, episode_id: int) -> Episode:
        episode = None
        try:
            episode = self._session_cm.session.query(Episode).get(episode_id)
        except NoResultFound:
            print("No episode found with id {}".format(episode_id))
        return episode

    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.merge(episode)
            scm.commit()

    def add_multiple_episodes(self, episode: List[Episode]):
        with self._session_cm as scm:
            for episode in episode:
                scm.session.merge(episode)
            scm.commit()

    def get_number_of_episodes(self):
        len_episodes = self._session_cm.session.query(Episode).count()
        return len_episodes

    def get_episodes_for_podcast(self, podcast_id: int) -> List[Episode]:
        """Get all episodes for a specific podcast by podcast_id."""
        episodes = self._session_cm.session.query(Episode).filter_by(podcast_id=podcast_id).all()
        return episodes

    def get_number_of_episodes_for_podcast(self, podcast_id: int) -> int:
        """ Returns the number of episodes for a particular podcast by podcast_id. """
        return len(self.get_episodes_for_podcast(podcast_id))

    # END REGION

    # CATEGORY REGION

    def get_category(self):
        categories = self._session_cm.session.query(Category).all()
        return categories

    def add_category(self, category: Category):
        with self._session_cm.session() as scm:
            scm.session.merge(category)
            scm.commit()

    def add_multiple_categories(self, categories: List[Category]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for category in categories:
                    scm.session.add(category)
            scm.commit()

    # END REGION

    # PLAYLIST REGION

    def add_ep_to_playlist(self, playlist_id, episode_id):
        with self._session_cm as scm:
            episode = self.get_episode(episode_id)
            self.get_playlist(playlist_id).add_episode(episode)
            scm.commit()

    def remove_ep_from_playlist(self, playlist_id, episode_id):
        with self._session_cm as scm:
            episode = self.get_episode(episode_id)
            self.get_playlist(playlist_id).remove_episode(episode)
            scm.commit()
            print("called")

    # END REGION

    # USER REGION

    def get_user(self, username: str):
        user = None
        try:
            user = self._session_cm.session.get(User, username)
        except NoResultFound:
            print("No User found with username {}".format(username))
        return user

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)

            scm.commit()


    def get_review(self, podcast_id: int):
        reviews = None
        try:
            reviews = self._session_cm.session.query(Review).filter(Review.podcast_id == podcast_id).all()
        except NoResultFound:
            print("No Review found with podcast id {}".format(podcast_id))
        return reviews

    # END REGION

    # SEARCH REGION

    def search_podcast_by_title(self, title_string: str) -> List[Podcast]:
        podcasts = self._session_cm.session.query(Podcast).filter(Podcast._title.ilike(f"%{title_string}%")).all()
        # Retrieve podcast whose title contains the title_string passed by the user.
        # This is a case-insensitive search without trailing spaces.
        return podcasts

    def search_podcast_by_author(self, author_name: str) -> List[Podcast]:
        try:
            author = self._session_cm.session.query(Author).filter(Author._name == author_name).all()
            podcasts = self._session_cm.session.query(Podcast).filter(Podcast._author == author[0]).all()
            return podcasts

        except IndexError:
            print("No Author found with name {}".format(author_name))
        return []

    def search_podcast_by_category(self, category_string: str) -> List[Podcast]:
        try:
            category = self._session_cm.session.query(Category).filter(Category._name == category_string)[0]
            podcasts_list = []
            podcasts = self._session_cm.session.query(Podcast).all()
            for podcast in podcasts:
                if category in podcast.categories:
                    podcasts_list.append(podcast)
            return podcasts_list
        except IndexError:
            print("No Category found with name {}".format(category_string))
            return []

