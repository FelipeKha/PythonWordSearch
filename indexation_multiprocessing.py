import os, re, multiprocessing
from functools import partial

class Indexation:

    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.index_dict = {}

    def indexation_of_file(self, index_dict, file_path):
        # pid = os.getpid()
        # print(f"Process id for {os.path.basename(file_path)}: {pid}")
        words_list = self._words_list_from_txt_file(file_path)
        index_dict = self._index_dict_construction(index_dict, words_list, file_path)
        return index_dict

    def indexation(self):
        manager = multiprocessing.Manager()
        index_dict_proxy = manager.dict(self.index_dict)

        func = partial(self.indexation_of_file, index_dict_proxy)

        pool = multiprocessing.Pool()
        pool.map(func, self.file_paths)
        pool.close()
        pool.join()

        self.index_dict = index_dict_proxy.copy()
        return self.index_dict

    @staticmethod
    def _words_list_from_txt_file(file_path):
        with open(file_path) as file:
            words_list = re.findall(r'\w+', file.read())
        return words_list

    @staticmethod
    def _index_dict_construction(index_dict, words_list, file_path):
        file_name = os.path.basename(file_path)
        for word in words_list:
            if word in index_dict:
                index_dict[word].add(file_name)
                if word == 'is':
                    print(index_dict[word])
            else:
                index_dict[word] = {file_name}
        return index_dict