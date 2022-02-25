import os, re, multiprocessing
from functools import partial

class Indexation:

    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.index_dict = {}

    def indexation(self):
        manager = multiprocessing.Manager()
        index_list_proxy = manager.list()

        lock = manager.Lock()

        func = partial(self.indexation_of_file, lock, index_list_proxy)

        pool = multiprocessing.Pool()
        pool.map(func, self.file_paths)
        pool.close()
        pool.join()

        index_dict = self._convert_index_list_proxy_to_dict(index_list_proxy)

        return index_dict

    def indexation_of_file(self, lock, index_list, file_path):
        # pid = os.getpid()
        # print(f"Process id for {os.path.basename(file_path)}: {pid}")
        words_list = self._words_list_from_txt_file(file_path)

        file_name = os.path.basename(file_path)
        for word in words_list:
            if word in index_list:
                lock.acquire()
                file_name_index = (index_list.index(word)+1) * -1
                index_list[file_name_index] = f"{index_list[file_name_index]}|{file_name}"
                lock.release()
            else:
                lock.acquire()
                index_list.insert(0, word)
                index_list.append(file_name)
                lock.release()

        return index_list

    @staticmethod
    def _words_list_from_txt_file(file_path):
        with open(file_path) as file:
            words_list = re.findall(r'\w+', file.read())
        return words_list

    @staticmethod
    def _convert_index_list_proxy_to_dict(index_list_proxy):
        number_of_word_in_index = int(len(index_list_proxy)/2)
        index_words_list = index_list_proxy[:number_of_word_in_index].copy()
        inverse_index_files_list = index_list_proxy[number_of_word_in_index:].copy()

        index_files_list = []
        for i in range(number_of_word_in_index):
            index_files_list.insert(0, inverse_index_files_list[i])

        temp_dict = dict(zip(index_words_list, index_files_list))
        index_dict = {}
        for key in temp_dict:
            files_list = temp_dict[key].split('|')
            index_dict[key] = set()
            for file in files_list:
                index_dict[key].add(file)

        return index_dict
