import podcast.episodes.services
from podcast.adapters.repository import AbstractRepository

from podcast.domainmodel.model import Playlist, User, Podcast, Episode


class NonExistentPlaylistException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_playlist(repo: AbstractRepository, user_name: str, playlist_name: str):
    user = repo.get_user(user_name)
    #if a playlist has been made already from the episodes/services.py
    try:
        playlist = repo.get_playlist(0)

    # if there is no user playlist
    except IndexError:
        if user is not None:
            playlist = Playlist(0, playlist_name, user)
            repo.add_playlist(playlist)
            return playlist
        else:
            raise UnknownUserException
    return playlist


def add_episode(repo: AbstractRepository, playlist_id: int, episode_id: int):
    playlist = repo.get_playlist(playlist_id)
    episode = repo.get_episode(episode_id)
    if playlist is None:
        raise NonExistentPlaylistException
    playlist.add_episode(episode)


def add_podcast(repo: AbstractRepository, playlist_id: int, podcast_id: int):
    playlist = repo.get_playlist(playlist_id)
    podcast = repo.get_podcast(podcast_id)
    if playlist is None:
        raise NonExistentPlaylistException
    playlist.add_podcast(podcast)


