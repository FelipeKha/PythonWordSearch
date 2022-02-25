import glob, os
import time


class IndexManagement:

    def __init__(self, search_folder_path, file_database_upper,
                 file_database_lower):
        self.search_folder_path = search_folder_path
        self.file_database_upper = file_database_upper
        self.file_database_lower = file_database_lower

        self.text_file_paths_list = []
        self.index_dict = {}

    def indexation_required(self):
        new_file_count = 0
        self.text_file_paths_list = \
            glob.glob(f"{self.search_folder_path}/*txt")
        if os.path.isfile(self.file_database_upper.index_file_path) and \
           os.path.isfile(self.file_database_lower.index_file_path):
            for file_path in self.text_file_paths_list:
                if os.path.getmtime(self.file_database_upper.index_file_path) < os.path.getmtime(file_path) or \
                   os.path.getmtime(self.file_database_lower.index_file_path) < os.path.getmtime(file_path):
                    new_file_count = new_file_count + 1
        else:
            new_file_count = 1

        return new_file_count > 0

    def jsons_creation(self, index_dict, indexation_time):
        index_dict = self._index_dict_conversion_from_set_to_list(index_dict)
        json_dict = self._json_dict_set_up(self.file_database_upper.index_file_path, index_dict, indexation_time)
        self.file_database_upper.save_dictionary(json_dict)
        self._json_lower_creation()

    def _json_lower_creation(self):
        t0 = time.time()
        json_dict_upper = self.file_database_upper.read_dictionary()
        index_dict_upper = json_dict_upper['index']
        index_dict_lower = self._conversion_index_to_lower(index_dict_upper)
        index_dict_lower = self._index_dict_conversion_from_set_to_list(index_dict_lower)
        t1 = time.time()
        indexation_time = t1-t0
        json_dict_lower = self._json_dict_set_up(self.file_database_lower.index_file_path,
                                                 index_dict_lower, indexation_time)
        self.file_database_lower.save_dictionary(json_dict_lower)

    @staticmethod
    def _json_dict_set_up(index_file_path, index_dict, indexation_time):
        json_dict = {}
        folder_indexed = os.path.basename(index_file_path)
        json_dict['meta_data'] = {'folder_indexed': folder_indexed,
                                  'indexation_time': indexation_time}
        json_dict['index'] = index_dict
        return json_dict

    @staticmethod
    def _index_dict_conversion_from_set_to_list(index_dict):
        for key in index_dict:
            index_dict[key] = list(index_dict[key])
        return index_dict

    @staticmethod
    def _conversion_index_to_lower(index_dict_upper):
        index_dict_lower = {}
        for key in index_dict_upper:
            key_low = key.lower()
            if key_low in index_dict_lower:
                index_dict_lower[key_low] = index_dict_lower[key_low].union(set(index_dict_upper[key]))
            else:
                index_dict_lower[key_low] = set(index_dict_upper[key])
        return index_dict_lower


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
