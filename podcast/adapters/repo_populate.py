import os, csv
from pathlib2 import Path

from podcast.adapters.repository import AbstractRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist


def populate(data_path: Path, repo: AbstractRepository, testing: bool = False):
    dir_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.'))
    if testing:
        # Different files for the testing mode.
        podcast_filename = os.path.join(dir_name, str(Path(data_path) / "podcasts_excerpt.csv"))
        episode_filename = os.path.join(dir_name, str(Path(data_path) / "episodes_excerpt.csv"))
    else:
        podcast_filename = os.path.join(dir_name, str(Path(data_path) / "podcasts.csv"))
        episode_filename = os.path.join(dir_name, str(Path(data_path) / "episodes.csv"))
    print(f"Podcast CSV: {podcast_filename}")
    print(f"Episode CSV: {episode_filename}")

    csv = CSVDataReader()
    podcast_csv = csv.get_podcastcsv()
    counter = 0

    list_podcasts = []
    list_episodes = []
    set_authors = set()
    set_categories = set()

    authors_dict = {}
    authors_count = 0
    categories_dict = {}
    categories_count = 1

    for row in podcast_csv:
        author_name = row[7]
        if not author_name:
            author_name = "Unknown"

        # if author has not been found yet
        if author_name not in authors_dict.keys():
            # add author to dict
            authors_dict[author_name] = authors_count
            authors_count += 1
            # create temp author
            temp_author = Author(authors_count, author_name)
            set_authors.add(temp_author)

        podcast_categories = row[5]
        temp_podcast = Podcast(row[0], temp_author, row[1], row[2], row[3], row[6], row[8], row[4])
        if podcast_categories:
            # Split into individual
            categories_split = podcast_categories.split('|')
            for category in categories_split:
                category = category.strip()
                temp_category = Category(categories_count, category)
                # temp_category.add_podcast(temp_podcast) doesnt work
                if category not in categories_dict.keys():
                    # add individual category to dict
                    categories_dict[category] = categories_count
                    categories_count += 1
                    # create temp category
                    set_categories.add(temp_category)
                else:
                    temp_category = next((cat for cat in set_categories if cat.name == category), None)
                temp_podcast.add_category(temp_category)

        list_podcasts.append(temp_podcast)


        counter += 1
    episode_csv = csv.get_episodecsv()
    podcasts = list_podcasts

    for row in episode_csv:
        # initializing temp podcast # !!!!!!!!!!!!!!!!!!!!!!!!!!!!! NEEDS TO BE CHANGED LATER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        temp_podcast = list_podcasts[0]
        # Finds the matching podcast for the episode using __eq__
        for podcast in podcasts:
            if podcast.id == row[1]:
                temp_podcast = podcast
                break
        for i in range(len(row)):
            if isinstance(row[i], int):
                if row[i] == "":
                    row[i] = 0
            if isinstance(row[i], str):
                if row[i] == "":
                    row[i] = "Unknown"
        # row[0] = id, row[1] = podcast_id, row[2] = title, row[3] = audio, row[4] = audio_length, row[5] = description, row[6] = pubdate
        temp_episode = Episode(row[0], temp_podcast, row[2], row[3], row[4], row[5], (row[6])[0:10])
        list_episodes.append(temp_episode)

    repo.add_multiple_authors(set_authors)
    repo.add_multiple_categories(set_categories)
    repo.add_multiple_podcasts(list_podcasts)
    repo.add_multiple_episodes(list_episodes)
