from file_database import FileDatabase


class Search:

    def __init__(self, word_searched, file_database_upper, file_database_lower):
        self.word_searched = word_searched
        self.file_database_upper = file_database_upper
        self.file_database_lower = file_database_lower

    def search_upper(self):
        index = self.file_database_upper.read_dictionary()
        result = self._search(self.word_searched, index)
        return result

    def search_lower(self):
        self.word_searched = self.word_searched.lower()
        index = self.file_database_lower.read_dictionary()
        result = self._search(self.word_searched, index)
        return result

    @staticmethod
    def _search(word_searched, index):
        if word_searched in index['index']:
            return index['index'][word_searched]
        else:
            return []