import os
import re


class Indexation:

    def __init__(self, file_paths):
        self.file_paths = file_paths

    def _indexation_function(self, index_dict, file_paths):
        for file_path in file_paths:
            pid = os.getpid()
            print(f"Process id for {file_path}: {pid}")
            words_list = self._words_list_from_txt_file(file_path)
            # lock.acquire()
            self._index_dict_construction(words_list, file_path, index_dict)
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
        file_name = os.path.basename(file_path)
        for word in words_list:
            if word in index_dict['index']:
                index_dict['index'][word].add(file_name)
            else:
                index_dict['index'][word] = {file_name}