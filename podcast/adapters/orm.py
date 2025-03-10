from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import registry, relationship
from datetime import datetime

from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist

# Global variable giving access to the MetaData (schema) information of the database
mapper_registry = registry()

authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('author_id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=False)
)

podcast_table = Table(
    'podcasts', mapper_registry.metadata,
    Column('podcast_id', Integer, primary_key=True),
    Column('title', Text, nullable=True),
    Column('image_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('language', String(255), nullable=True),
    Column('website_url', String(255), nullable=True),
    Column('author_id', ForeignKey('authors.author_id')),
    Column('itunes_id', Integer, nullable=True)
)

# Episodes should have links to its podcast through its foreign keys
episode_table = Table(
    'episodes', mapper_registry.metadata,
    Column('episode_id', Integer, primary_key=True),
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id')),
    Column('title', Text, nullable=True),
    Column('audio_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('pub_date', Text, nullable=True)
)

categories_table = Table(
    'categories', mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True, autoincrement=True),
    Column('category_name', String(64)) #, nullable=False)
)

podcast_categories_table = Table(
    'podcast_categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('category_id', ForeignKey('categories.category_id'))
)

users_table = Table(
    'users', mapper_registry.metadata,
    Column('id', Integer, autoincrement=True),
    Column('username', String(64), primary_key = True ,nullable=False),
    Column('password', String(64), nullable=False)
)

playlist_table = Table(
    'playlist', mapper_registry.metadata,
    Column('playlist_id', Integer, primary_key=True),
    Column('title', String(64), nullable=False),
    Column('owner_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('image', String(256)),
)

playlist_episodes_table = Table(
    'playlist_episodes', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('playlist_id', ForeignKey('playlist.playlist_id')),
    Column('episode_id', ForeignKey('episodes.episode_id')),
)

reviews_table = Table(
    'reviews', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('rating', Integer),
    Column('comment', Text)
)

def map_model_to_tables():

    mapper_registry.map_imperatively(Review, reviews_table, properties={
        '_id': reviews_table.c.id,
        '_podcast': relationship(Podcast, back_populates='_Podcast_reviews'),
        '_rating': reviews_table.c.rating,
        '_comment': reviews_table.c.comment,
        '_reviewer': relationship(User, back_populates='_User_reviews'),
    })

    mapper_registry.map_imperatively(Playlist, playlist_table, properties={
        '_id': playlist_table.c.playlist_id,
        '_title': playlist_table.c.title,
        '_owner': relationship('User', back_populates='playlists'),
        '_image': playlist_table.c.image,
        '_episodes': relationship(Episode, secondary=playlist_episodes_table, back_populates='playlists')
    })

    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_id': authors_table.c.author_id,
        '_name': authors_table.c.name,
    })

    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_id': categories_table.c.category_id,
        '_name': categories_table.c.category_name,
        'podcasts': relationship(Podcast, secondary=podcast_categories_table, back_populates='categories')
    })

    mapper_registry.map_imperatively(Podcast, podcast_table, properties={
        '_id': podcast_table.c.podcast_id,
        '_title': podcast_table.c.title,
        '_image': podcast_table.c.image_url,
        '_description': podcast_table.c.description,
        '_language': podcast_table.c.language,
        '_website': podcast_table.c.website_url,
        '_itunes_id': podcast_table.c.itunes_id,
        '_author': relationship(Author),
        '_Podcast_episodes': relationship(Episode, back_populates='_Episode__podcast'),
        'categories': relationship(Category, secondary=podcast_categories_table, back_populates='podcasts'),
        '_Podcast_reviews': relationship(Review, back_populates='_podcast'),
    })

    mapper_registry.map_imperatively(Episode, episode_table, properties={
        '_Episode__id': episode_table.c.episode_id,
        '_Episode__podcast': relationship(Podcast, back_populates='_Podcast_episodes'),
        '_Episode__title': episode_table.c.title,
        '_Episode__audio': episode_table.c.audio_url,
        '_Episode__description': episode_table.c.description,
        '_Episode__pub_date': episode_table.c.pub_date,
        'playlists': relationship(Playlist, secondary=playlist_episodes_table, back_populates='_episodes'),
    })

    mapper_registry.map_imperatively(User, users_table, properties={
        '_id': users_table.c.id,
        '_username': users_table.c.username,
        '_password': users_table.c.password,
        'playlists': relationship(Playlist, back_populates='_owner'),
        '_User_reviews': relationship(Review, back_populates='_reviewer')
    })



