from podcast.adapters.repository import AbstractRepository


def get_podcasts(repo: AbstractRepository):
    list_of_podcasts = []
    for i in range(1, 1000):
        podcast = repo.get_podcast(i)
        list_of_podcasts.append(podcast)
    return list_of_podcasts


def get_episodes(repo: AbstractRepository):
    list_of_episodes = []
    for i in range(5633):
        episode = repo.get_episode(i)
        list_of_episodes.append(episode)
    return list_of_episodes
