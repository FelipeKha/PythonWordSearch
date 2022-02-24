import json


class Search:

    def __init__(self, word_searched, index_file_path, index_no_cap_file_path):
        self.word_searched = word_searched
        self.index_file_path = index_file_path
        self.index_no_cap_file_path = index_no_cap_file_path

    def search_cap(self):
        index = self._load_index(self.index_file_path)
        return self._search(self.word_searched, index)

    def search_no_cap(self):
        self.word_searched = self.word_searched.lower()
        index = self._load_index(self.index_no_cap_file_path)
        return self._search(self.word_searched, index)

    # This is a static method, would be better to be taken out of the classes to uses across
    def _load_index(self, index_file_path):
      return json.load(open(index_file_path))

    def _search(self, word_searched, index):
        if word_searched in index['index']:
            return index['index'][word_searched]
        else:
            return []