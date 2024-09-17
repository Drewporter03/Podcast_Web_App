import podcast.playlists.services
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Playlist, Review

import datetime


class NonExistentPodcastException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_podcasts(repo: AbstractRepository):
    list_of_podcasts = []
    for i in range(0, 1000):
        podcast = repo.get_podcast(i)
        list_of_podcasts.append(podcast)
    return list_of_podcasts


def get_episodes(repo: AbstractRepository, podcast_id):
    list_of_episodes = []
    for i in range(1, 5633):
        episode = repo.get_episode(i)
        if episode.podcast_id == podcast_id:
            list_of_episodes.append(episode)
    return list_of_episodes


def sorted_episodes_by_date(repo: AbstractRepository, podcast_id):
    list_of_episodes = get_episodes(repo, podcast_id)
    return sorted(list_of_episodes, key=lambda episode: episode.date1)


def get_podcast_reviews(podcast_id, repo: AbstractRepository):
    podcast = repo.get_podcast(podcast_id)
    if podcast is None:
        raise NonExistentPodcastException

    return repo.get_review(podcast_id)


def get_average_reviews(podcast_id, repo: AbstractRepository):
    reviews = get_podcast_reviews(podcast_id, repo)
    if len(reviews) == 0:
        average = "N/A"
        return average
    average = 0
    for review in reviews:
        average += review.rating
    average /= len(reviews)
    average = round(average, 1)
    return average


def add_review(podcast_id, review_txt: str, review_rating: int, user_name: str, repo: AbstractRepository):
    podcast = repo.get_podcast(podcast_id)
    if podcast is not None:
        user = repo.get_user(user_name)
        if user is not None:
            review = Review(id(user), user, podcast, review_rating, review_txt)
            repo.add_review(review)
        elif user is None:
            raise UnknownUserException
    else:
        raise NonExistentPodcastException


# function to allow users to add episodes to a specific playlist
# right now we only have one playlist (playlist 0)
def playlist_add_episode(repo: AbstractRepository, playlist_id: int, episode_id: int):
    playlist = repo.get_playlist(playlist_id)
    episode = repo.get_episode(episode_id)
    if playlist is None:
        raise podcast.playlists.services.NonExistentPlaylistException
    playlist.add_episode(episode)
    print(playlist.podcast_list)


def get_user_playlist(repo: AbstractRepository):
    try:
        playlist = repo.get_playlist(0)
    # if the playlist has not been created yet there will be an index error
    except IndexError:
        return None
    return playlist


def add_playlist(repo: AbstractRepository, user_name: str, playlist_name: str):
    user = repo.get_user(user_name)
    if user is not None:
        playlist = Playlist(0, playlist_name, user)
        repo.add_playlist(playlist)
        return playlist
    else:
        raise UnknownUserException
