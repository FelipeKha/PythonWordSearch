import unittest, tempfile, os
from index_management import IndexManagement
from exceptions import NoTextFilesError, NoTargetDirectoryError
from file_database import FileDatabase

class ArtificialFileDatabase:

    def __init__(self, index_file_path):
        self.index_file_path = index_file_path


class TestIndexationRequired(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = self.temp_dir.name
        self.temp_txt_file_1 = tempfile.NamedTemporaryFile(suffix=".txt",
                             dir=self.temp_dir_path)

    def test_indexation_required_returns_true_when_new_folder_selected(self):
        self.artificial_file_database = ArtificialFileDatabase(self.temp_dir_path)
        index_management = IndexManagement(self.temp_dir_path,
                                           self.artificial_file_database, self.artificial_file_database)
        is_required = index_management.indexation_required()
        self.assertTrue(is_required)

    def test_indexation_required_returns_true_when_txt_file_has_changed(self):
        self.temp_index_file_1 = tempfile.NamedTemporaryFile(dir=self.temp_dir_path)
        self.temp_index_file_1_path = self.temp_index_file_1.name
        self.artificial_file_database = ArtificialFileDatabase(self.temp_index_file_1_path)
        self.temp_txt_file_2 = tempfile.NamedTemporaryFile(suffix=".txt",
                             dir=self.temp_dir_path)
        index_management = IndexManagement(self.temp_dir_path,
                                           self.artificial_file_database, self.artificial_file_database)
        is_required = index_management.indexation_required()
        self.assertTrue(is_required)
        self.temp_txt_file_2.close()
        self.temp_index_file_1.close()

    def test_indexation_required_returns_true_when_one_index_file_missing(self):
        self.temp_index_file_1 = tempfile.NamedTemporaryFile(dir=self.temp_dir_path)
        self.temp_index_file_1_path = self.temp_index_file_1.name
        self.artificial_file_database = ArtificialFileDatabase(self.temp_index_file_1_path)
        no_existing_file_path = f"{self.temp_dir_path}/non_existing_file.json"
        self.artificial_file_database_no_index = ArtificialFileDatabase(no_existing_file_path)
        index_management = IndexManagement(self.temp_dir_path,
                                           self.artificial_file_database, self.artificial_file_database_no_index)
        is_required = index_management.indexation_required()

        self.assertTrue(is_required)
        self.temp_index_file_1.close()

    def test_indexation_required_returns_false_when_txt_files_havent_changed(self):
        self.temp_index_file_1 = tempfile.NamedTemporaryFile(dir=self.temp_dir_path)
        self.temp_index_file_1_path = self.temp_index_file_1.name
        self.artificial_file_database = ArtificialFileDatabase(self.temp_index_file_1_path)
        index_management = IndexManagement(self.temp_dir_path,
                                           self.artificial_file_database, self.artificial_file_database)
        is_required = index_management.indexation_required()

        self.assertFalse(is_required)
        self.temp_index_file_1.close()

    def test_indexation_raises_NoTextFilesError_if_no_text_file_in_target_directory(self):
        temp_dir_no_txt = tempfile.TemporaryDirectory()
        temp_dir_no_txt_path = temp_dir_no_txt.name
        artificial_file_database_no_txt = ArtificialFileDatabase(temp_dir_no_txt_path)
        index_management = IndexManagement(temp_dir_no_txt_path,
                                           artificial_file_database_no_txt, artificial_file_database_no_txt)

        with self.assertRaises(NoTextFilesError):
            index_management.indexation_required()
        temp_dir_no_txt.cleanup()

    def test_indexation_required_raises_NoTargetDirectory_if_search_target_dir_doesnt_exist(self):
        temp_dir_path_no_dir = f"{self.temp_dir_path}/no_dir"
        self.artificial_file_database = ArtificialFileDatabase(self.temp_dir_path)
        index_management = IndexManagement(temp_dir_path_no_dir,
                                           self.artificial_file_database, self.artificial_file_database)
        with self.assertRaises(NoTargetDirectoryError):
            index_management.indexation_required()

    def test_indexation_required_returns_list_of_txt_files_from_searched_folder(self):
        self.artificial_file_database = ArtificialFileDatabase(self.temp_dir_path)
        index_management = IndexManagement(self.temp_dir_path,
                                           self.artificial_file_database, self.artificial_file_database)
        index_management.indexation_required()
        list_txt_files = index_management.text_file_paths_list
        self.assertEqual(list_txt_files, [self.temp_txt_file_1.name])


    def tearDown(self):
        self.temp_txt_file_1.close()
        self.temp_dir.cleanup()


class TestJsonCreation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = self.temp_dir.name
        self.temp_index_file_path_upper = f"{self.temp_dir_path}/upper.json"
        self.temp_index_file_path_lower = f"{self.temp_dir_path}/lower.json"
        self.file_database_upper = FileDatabase(self.temp_index_file_path_upper)
        self.file_database_lower = FileDatabase(self.temp_index_file_path_lower)

        self.index_management = IndexManagement(self.temp_dir_path,
                                                self.file_database_upper,
                                                self.file_database_lower)

        self.index_dict = {'is': {'text_1'},
                           'Is': {'text_1', 'text_2'},
                           'Other': {'text_3'}}
        self.index_dict_lower = {'is': {'text_1', 'text_2'},
                                 'other': {'text_3'}}
        self.indexation_time = 2.5

    def test_two_json_files_are_created(self):
        self.index_management.jsons_creation(self.index_dict,
                                             self.indexation_time)
        two_jsons_created = (os.path.isfile(self.temp_index_file_path_upper) and
                             os.path.isfile(self.temp_index_file_path_lower))

        self.assertTrue(two_jsons_created)

    def test_lower_json_contains_all_words_in_upper_json(self):
        self.index_management.jsons_creation(self.index_dict,
                                             self.indexation_time)
        dict_upper = self.file_database_upper.read_dictionary()
        dict_lower = self.file_database_lower.read_dictionary()

        all_word_from_upper_in_lower = True
        for key in dict_upper['index']:
            if key.lower() not in dict_lower['index']:
                all_word_from_upper_in_lower = False

        self.assertTrue(all_word_from_upper_in_lower)

    def test_lower_json_include_outputs_of_both_their_upper_and_lower_version(self):
        self.index_management.jsons_creation(self.index_dict,
                                             self.indexation_time)
        dict_upper = self.file_database_upper.read_dictionary()
        dict_lower = self.file_database_lower.read_dictionary()

        all_expected_output = True
        for key in dict_upper['index']:
            if key.lower() in dict_upper['index']:
                output_list = dict_upper['index'][key]
                output_list.extend(dict_upper['index'][key.lower()])
                output_set = set(output_list)
                for item in output_set:
                    if item not in dict_lower['index'][key.lower()]:
                        all_expected_output = False

        self.assertTrue(all_expected_output)

    def test_upper_json_contains_expected_content(self):
        self.index_management.jsons_creation(self.index_dict,
                                             self.indexation_time)
        dict_upper = self.file_database_upper.read_dictionary()
        index_dict_with_lists = {}

        for key in self.index_dict:
            index_dict_with_lists[key] = list(self.index_dict[key])

        self.assertEqual(dict_upper['index'], index_dict_with_lists)

    def test_lower_json_contains_expected_content(self):
        self.index_management.jsons_creation(self.index_dict,
                                             self.indexation_time)
        dict_lower = self.file_database_lower.read_dictionary()
        index_dict_lower_with_lists = {}

        for key in self.index_dict_lower:
            index_dict_lower_with_lists[key] = list(self.index_dict_lower[key])

        self.assertEqual(dict_lower['index'], index_dict_lower_with_lists)

    def tearDown(self):
        self.temp_dir.cleanup()


"""
indexation_required:
1. Indexation required because texts not indexed yet - OK
2. Indexation required because some text files have been saved after last 
indexation - OK
3. Indexation required because one of the index (upper or lower) is missing - OK
4. Indexation not required - OK
5. No text file in the target folder - OK
6. Target folder does not exist - OK
7. Correctly extract the list of .txt files from the target directory - OK

jsons_creation:
1. Two json files are created - OK
2. Lower json contains all words contained in upper - OK
3. Lower words contains the outputs for both their upper and lower version - OK
4. Upper json contains expected content - OK
5. Lower json contains expected content - OK
"""
