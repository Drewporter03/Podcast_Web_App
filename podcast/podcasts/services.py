from podcast.adapters.repository import AbstractRepository


def get_podcasts(repo: AbstractRepository):
    list_of_podcasts = []
    for i in range(1, 1000):
        podcast = repo.get_podcast(i)
        list_of_podcasts.append(podcast)
    return list_of_podcasts


def sorted_podcasts_by_title(repo: AbstractRepository):
    list_of_podcasts = get_podcasts(repo)
    return sorted(list_of_podcasts, key=lambda podcast: podcast.title)

def get_user_playlist(repo: AbstractRepository):
    try:
        playlist = repo.get_playlist(0)
    # if the playlist has not been created yet there will be an index error
    except IndexError:
        return None
    return playlist