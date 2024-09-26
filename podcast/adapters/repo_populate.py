import os, csv
from pathlib2 import Path

from podcast.adapters.repository import AbstractRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.memory_repository import get_podcastcsv, get_episodecsv, list_podcasts, list_episodes, \
    set_authors, set_categories, load_objects


def populate(data_path: Path, repo: AbstractRepository, testing: bool = False):
    dir_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.'))
    if testing:
        # Different files for the testing mode.
        podcast_filename = os.path.join(dir_name, str(Path(data_path) / "podcasts_excerpt.csv"))
        episode_filename = os.path.join(dir_name, str(Path(data_path) / "episodes_excerpt.csv"))
    else:
        podcast_filename = os.path.join(dir_name, str(Path(data_path) / "podcasts.csv"))
        episode_filename = os.path.join(dir_name, str(Path(data_path) / "episodes.csv"))

    load_objects()

    authors = set_authors
    categories = set_categories
    podcasts = list_podcasts
    episodes = list_episodes

    for author in authors:
        repo.add_author(author)

    for episode in episodes:
        repo.add_episode(episode)

    for podcast in podcasts:
        repo.add_podcast(podcast)

    for category in categories:
        repo.add_category(category)
