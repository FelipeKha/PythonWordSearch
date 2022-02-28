import os, re, multiprocessing
import time

class Indexation:

    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.index_dict = {}

    def indexation(self):
        nb_of_files_per_processor = \
            self._list_of_nb_files_per_processor(self.file_paths)
        list_files_for_each_processor = \
            self._split_path_list(self.file_paths, nb_of_files_per_processor)

        queue = multiprocessing.Queue()

        processes = []
        for item in list_files_for_each_processor:
            process = multiprocessing.Process(target=self.load_file_content_into_queue,
                                              args=(item, queue))
            processes.append(process)
            process.start()

        index_dict = self._from_queue_to_index_dict(queue,
                                                    len(list_files_for_each_processor))

        for item in processes:
            item.join()
            # print(f"all processes close at: {time.time()}")


        return index_dict

    def load_file_content_into_queue(self, file_paths, queue):
        # pid = os.getpid()
        # print(f"Process id for {file_paths}: {pid}")
        for file in file_paths:
            file_content = self._load_file_content(file)
            file_name = os.path.basename(file)
            queue.put((file_name, file_content))
                # if queue.full():
                #     print("Queue is full")
        queue.put(None)

    @staticmethod
    def _load_file_content(file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()
            file.close()
        return file_content

    @staticmethod
    def _words_list_from_string(string):
        words_list = re.split(r'\W+', string)
        return words_list

    def _from_queue_to_index_dict(self, queue, nb_processors):
        index_dict = {}
        nb_marker = 0
        while True:
            item = queue.get()
            # print(item)
            if item == None:
                nb_marker += 1
                if nb_marker == nb_processors:
                    break
            else:
                file_name = item[0]
                word_list = self._words_list_from_string(item[1])
                for word in word_list:
                    if word in index_dict:
                        index_dict[word].add(file_name)
                    else:
                        index_dict[word] = {file_name}
        # print("Queue finished")
        # print(f"Index ready at: {time.time()}")
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