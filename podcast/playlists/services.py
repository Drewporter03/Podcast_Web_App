import podcast.episodes.services
from podcast.adapters.repository import AbstractRepository

from podcast.domainmodel.model import Playlist, User, Podcast, Episode


class PlaylistNotFoundException(Exception):
    pass


class EpisodeNotFoundException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class NonExistentPodcastException(Exception):
    pass


def add_playlist(repo: AbstractRepository, user_name: str, playlist_name: str):
    user = repo.get_user(user_name)
    if not user:
        raise UnknownUserException(f"{user_name} not found.")
    try:
        playlist = get_user_playlist(repo, 0)
    except PlaylistNotFoundException:
        playlist = Playlist(0, playlist_name, user)
        repo.add_playlist(playlist)
    return playlist


def get_user_playlist(repo: AbstractRepository, playlist_id: int):
    try:
        playlist = repo.get_playlist(0)
    # if the playlist has not been created yet there will be an index error
    except IndexError:
        raise PlaylistNotFoundException(f"Playlist with ID {playlist_id} not found.")
    return playlist


def add_episode(repo: AbstractRepository, playlist_id: int, episode_id: int):
    playlist = repo.get_playlist(playlist_id)
    if not playlist:
        raise PlaylistNotFoundException(f"Playlist with ID {playlist_id} not found.")
    episode = repo.get_episode(episode_id)
    if not episode:
        raise EpisodeNotFoundException(f"Episode with ID {episode_id} not found.")

    playlist.add_episode(episode)


def add_podcast(repo: AbstractRepository, playlist_id: int, podcast_id: int):
    playlist = repo.get_playlist(playlist_id)
    if not playlist:
        raise PlaylistNotFoundException(f"Playlist with ID {playlist_id} not found.")
    podcast = repo.get_podcast(podcast_id)
    if not podcast:
        raise NonExistentPodcastException(f"podcast with ID {podcast_id} not found.")
    episodes = get_episodes(repo, podcast_id)
    for episode in episodes:
        add_episode(repo, playlist_id, episode._id)


def remove_episode(repo: AbstractRepository, playlist_id: int, episode_id: int):
    episode = repo.get_episode(episode_id)
    if not episode:
        raise EpisodeNotFoundException(f"Episode with ID {episode_id} not found.")
    playlist = repo.get_playlist(playlist_id)
    if not playlist:
        raise PlaylistNotFoundException(f"Playlist with ID {playlist_id} not found.")
    if episode in playlist.podcast_list:
        playlist.remove_episode(episode)


def get_episodes(repo: AbstractRepository, podcast_id):
    list_of_episodes = []
    for i in range(1, 5633):
        episode = repo.get_episode(i)
        if episode.podcast_id == podcast_id:
            list_of_episodes.append(episode)
    return list_of_episodes
