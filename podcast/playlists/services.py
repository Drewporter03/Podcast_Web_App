from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Playlist


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

        user_id = user.id
        playlist = get_user_playlist(repo, user_id)

    except PlaylistNotFoundException:
        user_id = user.id
        playlist = Playlist(user_id, playlist_name, user)
        repo.add_playlist(playlist)

    return playlist


def get_user_playlist(repo: AbstractRepository, user_id: int):
    playlist = repo.get_playlist(user_id)
    # if the playlist has not been created it will be none
    if not playlist:
        raise PlaylistNotFoundException(f"Playlist with ID {user_id} not found.")
    return playlist


def add_episode(repo: AbstractRepository, playlist_id: int, episode_id: int):
    playlist = repo.get_playlist(playlist_id)
    if not playlist:
        raise PlaylistNotFoundException(f"Playlist with ID {playlist_id} not found.")
    if repo.get_episode(episode_id) == None:
        raise EpisodeNotFoundException(f"Episode with ID {episode_id} not found.")
    episode = repo.get_episode(episode_id)
    repo.add_ep_to_playlist()
    playlist.add_episode(episode)


def add_podcast(repo: AbstractRepository, playlist_id: int, podcast_id: int):
    # method adds all episodes from a podcast
    playlist = repo.get_playlist(playlist_id)
    if not playlist:
        raise PlaylistNotFoundException(f"Playlist with ID {playlist_id} not found.")
    podcast = repo.get_podcast(podcast_id)
    if repo.get_podcast(podcast_id) == None:
        raise NonExistentPodcastException(f"podcast with ID {podcast_id} not found.")
    podcast = repo.get_podcast(podcast_id)
    episodes = get_episodes(repo, podcast_id)
    for episode in episodes:
        add_episode(repo, playlist_id, episode.id)


def remove_episode(repo: AbstractRepository, playlist_id: int, episode_id: int):
    episode = repo.get_episode(episode_id)
    if not episode:
        raise EpisodeNotFoundException(f"Episode with ID {episode_id} not found.")
    playlist = repo.get_playlist(playlist_id)
    if not playlist:
        raise PlaylistNotFoundException(f"Playlist with ID {playlist_id} not found.")
    if episode in playlist._episodes:
        playlist.remove_episode(episode)


def get_episodes(repo: AbstractRepository, podcast_id):
    # REMOVE - CAN CALL FROM BP
    return repo.get_episodes_for_podcast(podcast_id)


def get_user(repo: AbstractRepository, user_name: str):
    # used for creating user playlists
    return repo.get_user(user_name)
