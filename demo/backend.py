import glob, json, os, re
from pathlib import Path
from time import process_time
import multiprocessing
from functools import partial


class FileDatabase:
    def __init__(self, db_file_path):
        self._file_path = db_file_path
        self._last_modified = None

    def save_dictionary(self, dict):
        index_json = json.dumps(dict)
        index_file = open(self._file_path, "w")
        index_file.write(index_json)
        index_file.close()

    def read_dictionary(self):
        try:
            index = json.load(open(self._file_path))
            return index
        except FileNotFoundError:
            raise DictionaryNotSavedException()

    def last_modified(self):
        return self._last_modified


class DictionaryNotSavedException(Exception):
    pass
    
    
class BetterDatabase:
    def save_dictionary(self, dict):
        pass

    def read_dictionary(self):
        pass


class Index:
    def __init__(self, search_folder_path, database, database_no_cap):
        self.target_directory_path = search_folder_path
        self.file_paths = []
        self.database = database
        self.database_no_cap = database_no_cap

    def indexation_required(self):
        new_file_count = 0
        self.file_paths = glob.glob(f"{self.target_directory_path}/*txt")
        if os.path.isfile(self._index_file_path) and os.path.isfile(self._index_no_cap_file_path):
            for file_path in self.file_paths:
                if os.path.getmtime(self._index_file_path) < os.path.getmtime(file_path) or os.path.getmtime(self._index_no_cap_file_path) < os.path.getmtime(file_path):
                    new_file_count = new_file_count + 1
        else:
            new_file_count = 1

        return new_file_count > 0

    def index_creation(self):
        print("Indexation started")
        t0 = process_time()
        index_dict = self._index_dict_set_up(self._index_file_path)
        indexation = Indexation(self.file_paths, index_dict)
        index_dict = indexation._perform_indexation()
        index_dict = self._index_dict_conversion_from_set_to_list(index_dict)
        t1 = process_time()
        elapsed_time = t1 - t0
        index_dict['meta_data']['indexation_time'] = elapsed_time
        self.database.save_dictionary(index_dict)
        self._index_no_cap()
        print("Indexation ended")
        print(f"Indexation time of {self._get_indexation_time(self._index_file_path) + self._get_indexation_time(self._index_no_cap_file_path)} seconds ({self._get_indexation_time(self._index_file_path)} for initial index, {self._get_indexation_time(self._index_no_cap_file_path)} for no_cap index)")

    def _index_no_cap(self):
        t0 = process_time()
        index_cap = self.database.read_dictionary()
        index_no_cap = self._index_dict_set_up(self._index_no_cap_file_path)
        index_no_cap = self._conversion_index_to_no_cap(index_cap, index_no_cap)
        index_no_cap = self._index_dict_conversion_from_set_to_list(index_no_cap)
        t1 = process_time()
        elapsed_time = t1 - t0
        index_no_cap['meta_data']['indexation_time'] = elapsed_time
        self.database_no_cap.save_dictionary(index_no_cap)

    # Static method
    def _index_dict_set_up(self, index_file_path):
        index_dict = {}
        index_dict['meta_data'] = {'folder_indexed': index_file_path}
        index_dict['index'] = {}
        return index_dict

    def _index_dict_conversion_from_set_to_list(self, index_dict):
        for key in index_dict['index']:
            index_dict['index'][key] = list(index_dict['index'][key])
        return index_dict

    def _conversion_index_to_no_cap(self, index_cap, index_no_cap):
        for key in index_cap['index']:
            key_low = key.lower()
            if key_low in index_no_cap['index']:
                index_no_cap['index'][key_low] = index_no_cap['index'][key_low].union(set(index_cap['index'][key]))
            else:
                index_no_cap['index'][key_low] = set(index_cap['index'][key])
        return index_no_cap

    def _get_indexation_time(self, index_file_path):
        return json.load(open(index_file_path))['meta_data']['indexation_time']



class Indexation:

    def __init__(self, file_paths, index_dict):
        self.file_paths = file_paths
        self.index_dict = index_dict

    def _indexation_function(self, index_dict, file_paths):
        for file_path in file_paths:
            pid = os.getpid()
            print(f"Process id for {file_path}: {pid}")
            words_list = self._words_list_from_txt_file(file_path)
            # lock.acquire()
            index_dict = self._index_dict_construction(words_list, file_path, index_dict)
            # lock.release()
        return index_dict

    def _perform_indexation(self):

        self.index_dict = self._indexation_function(self. index_dict, self.file_paths)


        # manager = multiprocessing.Manager()
        # index_dict = manager.dict(self.index_dict)
        #
        # pool = multiprocessing.Pool()
        # # manager = multiprocessing.Manager()
        # # lock = manager.Lock()
        #
        # func = partial(self._indexation_function, index_dict)
        #
        # pool.map(func, self.file_paths)
        # pool.close()
        # pool.join()
        # print(index_dict)
        return self.index_dict

    def _words_list_from_txt_file(self, file_path):
        with open(file_path) as file:
            words_list = re.findall(r'\w+', file.read())
        return words_list

    def _index_dict_construction(self, words_list, file_path, index_dict):
        for word in words_list:
            if word in index_dict['index']:
                index_dict['index'][word].add(file_path)
            else:
                index_dict['index'][word] = {file_path}
        return index_dict


class Search:
    def __init__(self, word_searched, database, database_no_cap):
        self.word_searched = word_searched
        self._database = database
        self._database_no_cap = database_no_cap

    def search_cap(self):
        index = self._database.read_dictionary()
        return self._search(self.word_searched, index)

    def search_no_cap(self):
        self.word_searched = self.word_searched.lower()
        index = self._database_no_cap.read_dictionary()
        return self._search(self.word_searched, index)

    # # This is a static method, would be better to be taken out of the classes to uses across
    # def _load_index(self, index_file_path):
    #   return json.load(open(index_file_path))

    @staticmethod
    def _search(word_searched, index):
        if word_searched in index['index']:
            return index['index'][word_searched]
        else:
            return []






"""
Make the indexation at least 10 times faster
Fix "case insensitive search"
Fix the "what if i search for Folder_Indexed"?
Add unit tests to verify behaviour of Index and Search
Use private methods to have nice to read methods with similar levels of abstraction inside
Study the data structure called Set and make use of it in the code
Use class instance variables to simplify the class methods when used
Return same types from a given function

'is' search should return doc 1
Should we do class inheritance to avoid two _lead_index methods?

My pool method for multiprocessing return a list. Is taking the only element of the list as the result the right way to do it?
"""
