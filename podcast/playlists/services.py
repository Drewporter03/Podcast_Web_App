from podcast.adapters.repository import AbstractRepository

from podcast.domainmodel.model import Playlist, User, Podcast, Episode


class NonExistentPlaylistException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_episodes(repo: AbstractRepository, podcast_id):
    list_of_episodes = []
    for i in range(1, 5633):
        episode = repo.get_episode(i)
        if episode.podcast_id == podcast_id:
            list_of_episodes.append(episode)
    return list_of_episodes



def add_playlist(repo: AbstractRepository, user_name: str, playlist_name: str):
    user = repo.get_user(user_name)
    if user is not None:
        playlist = Playlist(0, playlist_name, user)
        repo.add_playlist(playlist)
    else:
        raise UnknownUserException


def add_episode(repo: AbstractRepository, playlist_id: int, episode_id: int):
    playlist = repo.get_playlist(playlist_id)
    episode = repo.get_episode(episode_id)
    print(episode.podcast_id)
    print(repo.get_podcast(episode.podcast_id))
    if playlist is None:
        raise NonExistentPlaylistException
    playlist.add_episode(episode)

    print(playlist.podcast_list)
