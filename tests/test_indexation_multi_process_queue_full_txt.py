import unittest, tempfile, os
from indexation_multi_process_queue_full_txt import Indexation

class TestIndexation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = self.temp_dir.name
        self.files_list = []
        self.file_paths_list = []
        self.file_names_set = set()
        self.test_word_1 = "Testwordone"
        self.test_word_2 = "Testwordtwo"
        self.result_dict = {}
        for i in range(10):
            temp_txt_file = tempfile.NamedTemporaryFile(suffix=".txt",
                                                        dir=self.temp_dir_path)
            temp_txt_file_path = temp_txt_file.name
            self.files_list.append(temp_txt_file)
            self.file_paths_list.append(temp_txt_file_path)

        for file_path in self.file_paths_list:
            temp_txt_file_name = os.path.basename(file_path)
            with open(file_path, "w") as file:
                if self.file_paths_list.index(file_path) <= 4:
                    file.write(self.test_word_1)
                    if self.test_word_1 in self.result_dict:
                        self.result_dict[self.test_word_1].add(temp_txt_file_name)
                    else:
                        self.result_dict[self.test_word_1] = {temp_txt_file_name}
                else:
                    file.write(self.test_word_2)
                    if self.test_word_2 in self.result_dict:
                        self.result_dict[self.test_word_2].add(temp_txt_file_name)
                    else:
                        self.result_dict[self.test_word_2] = {temp_txt_file_name}
            self.file_names_set.add(temp_txt_file_name)

        self.indexation = Indexation(self.file_paths_list)

    def test_indexation_returns_dict_with_all_words_from_text_files(self):
        indexation_return = self.indexation.indexation()
        words_list = list(indexation_return.keys())
        words_list.sort()
        expected_words_list = [self.test_word_1, self.test_word_2]
        expected_words_list.sort()

        self.assertEqual(words_list, expected_words_list)

    def test_indexation_returns_dict_with_words_from_all_texts_files(self):
        indexation_return = self.indexation.indexation()
        texts_from_indexation_set = set()
        for key in indexation_return:
            for item in indexation_return[key]:
                texts_from_indexation_set.add(item)

        self.assertEqual(self.file_names_set, texts_from_indexation_set)

    def test_indexation_returns_expected_dict(self):
        indexation_return = self.indexation.indexation()

        self.assertEqual(self.result_dict, indexation_return)


    def tearDown(self):
        for file in self.files_list:
            file.close()
        self.temp_dir.cleanup()

"""
indexation:
1. Returns dict with all words from text files - OK
2. Returns dict with words from all texts files - OK
3. Returns expected dict - OK
"""