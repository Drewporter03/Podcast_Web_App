import os
import csv
from podcast.domainmodel.model import Podcast, Episode, Author, Category


class CSVDataReader:
    def __init__(self):
        # initialising lists to append to later, for info keeping
        self.__podcasts = []
        self.__episodes = []
        self.__authors = {}
        self.__categories = {}

    def csv_read(self, filename: str):
        # reading csv file using module csv
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                row = [info.strip() for info in row]
                self.__episodes.append(row)
        return

    def get_episodes(self):
        self.csv_read('episodes.csv')
        for row in self.__episodes:
            Episode(row[0], row[2], row[4], row[4])



