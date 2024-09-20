import csv
from pathlib import Path


class CSVDataReader:
    def __init__(self):
        return

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

