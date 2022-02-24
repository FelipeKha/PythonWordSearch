import json


class FileDatabase:
    def __init__(self, index_file_path):
        self.index_file_path = index_file_path

    def save_dictionary(self, dict):
        index_json = json.dumps(dict)
        index_file = open(self.index_file_path, "w")
        index_file.write(index_json)
        index_file.close()

    def read_dictionary(self):
        index = json.load(open(self.index_file_path))
        return index

    def read_indexation_time(self):
        index = json.load(open(self.index_file_path))
        return index['meta_data']['indexation_time']