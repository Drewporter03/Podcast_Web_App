import os
import csv
from podcast.domainmodel.model import Podcast, Episode, Author, Category
from pathlib import Path


class CSVDataReader:
    def __init__(self):
        # initialising lists to append to later, for info keeping
        self.__podcasts = []
        self.__episodes = []
        self.__authors = {}
        self.__categories = {}

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
            podcast_list.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
        return podcast_list

    def get_episodecsv(self):
        file_path = Path(__file__).resolve().parents[1] / 'data' / 'episodes.csv'
        info_list = self.csv_read(file_path)

        episode_list = []
        for row in info_list:
            # row[0] = id, row[1] = podcast_id, row[2] = title, row[3] = audio, row[4] = audio_length, row[5] = description, row[6] = pubdate
            episode_list.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
        return episode_list

