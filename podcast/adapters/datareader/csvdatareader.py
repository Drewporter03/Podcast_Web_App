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

    def get_podcast(self):
        file_path = Path(__file__).resolve().parents[1] / 'data' / 'podcasts.csv'
        info_list = self.csv_read(file_path)

        for row in info_list:
            pass

    def get_episode(self):
        file_path = Path(__file__).resolve().parents[1] / 'data' / 'episodes.csv'
        info_list = self.csv_read(file_path)

        for row in info_list:
            pass





