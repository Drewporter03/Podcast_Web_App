import os
import csv
from podcast.domainmodel.model import Podcast, Episode, Author, Category
from pathlib import Path


class CSVDataReader:
    def __init__(self):
        # initialising lists to append to later, for info keeping
        self.__podcasts = []
        self.__episodes = []
        self.__authors = set()
        self.__categories = set()

        # calling both functions to fill in the sets and lists
        self.author_object()
        self.podcast_object()
        self.episode_object()
        self.categories_object()

    def csv_read(self, path: Path):
        # reading csv file using module csv
        info_list = []
        with path.open() as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                row = [info.strip() for info in row]
                info_list.append(row)
        # return everything except first, first row is just identifiers
        return info_list[1:]

    def get_podcastcsv(self):
        file_path = Path(__file__).resolve().parents[1] / 'data' / 'podcasts.csv'
        info_list = self.csv_read(file_path)

        podcast_list = []
        for row in info_list:
            # row[0] = id, row[1] = title, row[2] = image, row[3] = description, row[4] = language, row[5] = categories, row[6] = website, row[7] = author, row[8] = itunes_id
            podcast_list.append([int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], int(row[8])])
        return podcast_list

    def get_episodecsv(self):
        file_path = Path(__file__).resolve().parents[1] / 'data' / 'episodes.csv'
        info_list = self.csv_read(file_path)

        episode_list = []
        for row in info_list:
            # row[0] = id, row[1] = podcast_id, row[2] = title, row[3] = audio, row[4] = audio_length, row[5] = description, row[6] = pubdate
            episode_list.append([int(row[0]), int(row[1]), row[2], row[3], int(row[4]), row[5], row[6]])
        return episode_list

    def author_object(self):
        podcast_csv = CSVDataReader.get_podcastcsv(self)
        for row in podcast_csv:
            if row[7] != "":
                temp_author = Author(id(row[7]), row[7])
            else:
                temp_author = Author(id(row[7]), "unknown")
            self.__authors.add(temp_author)

    def podcast_object(self):
        podcast_csv = CSVDataReader.get_podcastcsv(self)
        author = self.__authors

        for row in podcast_csv:
            if row[7] != "":
                temp_author = Author(id(row[7]), row[7])
            else:
                temp_author = Author(id(row[7]), "Unknown")

            if temp_author in author:
                pass
            else:
                self.__authors.add(temp_author)

            temp_podcast = Podcast(row[0], temp_author, row[1], row[2], row[3], row[6], row[8], row[4])
            self.__podcasts.append(temp_podcast)

    def categories_object(self):
        podcast_csv = CSVDataReader.get_podcastcsv(self)
        for row in podcast_csv:
            if row[5] != "":
                temp_category = Category(id(row[5]), row[5])
            else:
                temp_category = Category(id(row[5]), "Unknown")
            self.__categories.add(temp_category)

    def episode_object(self):
        podcast_csv = CSVDataReader.get_podcastcsv(self)
        episode_csv = CSVDataReader.get_episodecsv(self)
        for row in episode_csv:
            podcasts = self.__podcasts
            temp_podcast = self.__podcasts[0]
            # Finds the matching podcast for the episode using __eq__
            for podcast in podcasts:
                if podcast == row[1]:
                    temp_podcast = podcast
            for i in range(len(row)):
                if isinstance(row[i], int):
                    if row[i] == "":
                        row[i] = 0
                if isinstance(row[i], str):
                    if row[i] == "":
                        row[i] = "Unknown"
            # row[0] = id, row[1] = podcast_id, row[2] = title, row[3] = audio, row[4] = audio_length, row[5] = description, row[6] = pubdate
            temp_episode = Episode(row[0], row[1], row[2], row[3], row[4], (row[6])[0:10], row[5], temp_podcast)
            self.__episodes.append(temp_episode)

    @property
    def authors(self):
        return self.__authors

    @property
    def podcasts(self):
        return self.__podcasts

    @property
    def category(self):
        return self.__categories

    @property
    def episodes(self):
        return self.__episodes

