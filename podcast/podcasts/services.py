import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository, populate
from podcast.adapters.repository import AbstractRepository

def get_podcasts(repo: AbstractRepository):
    list_of_podcasts = []
    for i in range(1, 1000):
        podcast = repo.get_podcast(i)
        list_of_podcasts.append(podcast)
    return list_of_podcasts

