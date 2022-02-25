import os, re, multiprocessing
from functools import partial

class Indexation:

    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.index_dict = {}

    def indexation(self):
        nb_of_files_per_processor = \
            self._list_of_nb_files_per_processor(self.file_paths)
        list_files_for_each_processor = \
            self._split_path_list(self.file_paths, nb_of_files_per_processor)

        manager = multiprocessing.Manager()
        index_list_proxy = manager.list()

        lock = manager.Lock()

        processes = []
        for item in list_files_for_each_processor:
            process = multiprocessing.Process(target=self.indexation_of_file,
                                              args=(lock, index_list_proxy, item))
            processes.append(process)
            process.start()

        for item in processes:
            item.join()

        index_dict = self._convert_index_list_proxy_to_dict(index_list_proxy)

        return index_dict

    def indexation_of_file(self, lock, index_list, file_paths):
        pid = os.getpid()
        print(f"Process id for {file_paths}: {pid}")
        for file in file_paths:
            words_list = self._words_list_from_txt_file(file)

            file_name = os.path.basename(file)
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

    @staticmethod
    def _list_of_nb_files_per_processor(file_paths_list):
        number_processors = multiprocessing.cpu_count()
        nb_file_per_processor_list = []

        number_txt_per_processor_pre_remainder = \
            int(len(file_paths_list) / number_processors)
        remainder = len(file_paths_list) % number_processors

        count = number_processors
        while True:
            number_txt_for_processor = number_txt_per_processor_pre_remainder + min(remainder, 1)
            nb_file_per_processor_list.append(number_txt_for_processor)
            remainder = max(remainder - 1, 0)
            count -= 1
            if count == 0:
                break

        return nb_file_per_processor_list

    @staticmethod
    def _split_path_list(file_paths_list, nb_file_per_processor_list):
        list_files_for_each_processor = []
        for item in nb_file_per_processor_list:
            list_files_for_each_processor.append(file_paths_list[:item])
            del file_paths_list[:item]
        return list_files_for_each_processor