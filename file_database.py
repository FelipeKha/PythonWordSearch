import json, os

from exceptions import NoIndexDirectoryError, NoIndexFileError

class FileDatabase:
    def __init__(self, index_file_path):
        self.index_file_path = index_file_path

    def save_dictionary(self, dict):
        index_dir_path = os.path.dirname(self.index_file_path)
        if not os.path.isdir(index_dir_path):
            raise NoIndexDirectoryError

        index_json = json.dumps(dict)
        index_file = open(self.index_file_path, "w")
        index_file.write(index_json)
        index_file.close()

    def read_dictionary(self):
        if not os.path.isfile(self.index_file_path):
            raise NoIndexFileError

        with open(self.index_file_path) as file:
            index = json.load(file)
            file.close()
        return index

    def read_indexation_time(self):
        if not os.path.isfile(self.index_file_path):
            raise NoIndexFileError

        with open(self.index_file_path) as file:
            index = json.load(file)
            file.close()
        return index['meta_data']['indexation_time']

class DictionaryNotSavedException(Exception):
    pass