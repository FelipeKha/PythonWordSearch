import os
import re


class Indexation:

    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.index_dict = {}

    def indexation(self):
        for file_path in self.file_paths:
            pid = os.getpid()
            print(f"Process id for {os.path.basename(file_path)}: {pid}")
            words_list = self._words_list_from_txt_file(file_path)
            self._index_dict_construction(words_list, file_path)
        return self.index_dict

    @staticmethod
    def _words_list_from_txt_file(file_path):
        with open(file_path) as file:
            words_list = re.findall(r'\w+', file.read())
        return words_list

    def _index_dict_construction(self, words_list, file_path):
        file_name = os.path.basename(file_path)
        for word in words_list:
            if word in self.index_dict:
                self.index_dict[word].add(file_name)
            else:
                self.index_dict[word] = {file_name}