import unittest, os, json

from demo.backend import Index, Search, FileDatabase

class TestIndexationRequired(unittest.TestCase):
    def test_indexation_required_returns_true_when_new_folder_selected(self):
        # Given
        search_folder_path = '/non_existing_folder'
        index = Index(search_folder_path)

        # When
        is_required = index.indexation_required()

        # Then
        self.assertTrue(is_required)

    def test_indexation_required_returns_true_when_txt_file_has_changed(self):
        # Given
        search_folder_path = './documents'
        index = Index(search_folder_path)
        index.index_creation()
        temp_text_file_content = "test"
        temp_text_path_for_save_after = f"{search_folder_path}/temp_text_file_for_save_after.txt"
        with open(temp_text_path_for_save_after, "w") as file:
            file.write(temp_text_file_content)

        # When
        is_required = index.indexation_required()

        # Then
        self.assertTrue(is_required)
        os.remove(temp_text_path_for_save_after)

    def test_indexation_required_returns_false_when_txt_files_havent_changed(self):
        # Given
        search_folder_path = './documents'
        index = Index(search_folder_path)
        index.index_creation()

        # When
        is_required = index.indexation_required()

        # Then
        self.assertFalse(is_required)

class TestIndexCreation(unittest.TestCase):

    def setUp(self):
        self.search_folder_path = './documents'
        self.index = Index(self.search_folder_path)

        self.index_file_path_upper = f"./demo/{os.path.basename(self.index._index_file_path)}"
        self.index_file_path_lower = f"./demo/{os.path.basename(self.index._index_no_cap_file_path)}"

    def test_index_creation_creates_two_json_files(self):
        os.remove(self.index._index_file_path)
        os.remove(self.index._index_no_cap_file_path)

        self.index.index_creation()

        self.assertTrue(os.path.isfile(self.index._index_file_path) and \
                        os.path.isfile(self.index._index_no_cap_file_path))

    def test_index_creation_no_cap_index_is_entirely_lowercap(self):
        self.index.index_creation()
        number_of_cap = 0
        json_content = json.load(open(self.index._index_no_cap_file_path))
        for key in json_content['index']:
            if key.lower() != key:
                number_of_cap += 1
        self.assertTrue(number_of_cap == 0)

    def test_index_creation_save_word_from_txt(self):
        temp_text_file_content = "WeirdContentForTestOnly"
        temp_text_path_for_weird_word = f"{self.search_folder_path}/temp_text_file_for_weird_word.txt"
        with open(temp_text_path_for_weird_word, "w") as file:
            file.write(temp_text_file_content)

        self.index.index_creation()
        print(self.index._index_file_path)

        json_content_upper = json.load(open(self.index._index_file_path))
        json_content_lower = json.load(open(self.index._index_no_cap_file_path))

        self.assertTrue(temp_text_file_content in json_content_upper['index'] and \
                        temp_text_file_content.lower() in json_content_lower['index'])
        os.remove(temp_text_path_for_weird_word)

    def tearDown(self):
        pass

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.upper_index_file_path = './upper_index_for_search_test.json'
        self.lower_index_file_path = './lower_index_for_search_test.json'

        index_dict_upper = {'index': {}}
        index_dict_lower = {'index': {}}
        self.temp_text_file_content = "WeirdContentForTestOnly"
        self.fictitious_txt_file_name = "fictitious_file.txt"
        index_dict_upper['index'][self.temp_text_file_content] = self.fictitious_txt_file_name
        index_dict_lower['index'][self.temp_text_file_content.lower()] = self.fictitious_txt_file_name

        self.upper_file_database = FileDatabase(self.upper_index_file_path)
        self.lower_file_database = FileDatabase(self.lower_index_file_path)
        self.upper_file_database.save_dictionary(index_dict_upper)
        self.lower_file_database.save_dictionary(index_dict_lower)

        self.search = Search(self.temp_text_file_content, self.upper_index_file_path,
                             self.lower_index_file_path)

    def test_search_cap_returns_expected_result(self):
        self.assertEqual(self.search.search_cap(), self.fictitious_txt_file_name)

    def test_search_no_cap_returns_expected_result(self):
        self.assertEqual(self.search.search_no_cap(), self.fictitious_txt_file_name)

    def tearDown(self):
        os.remove(self.upper_index_file_path)
        os.remove(self.lower_index_file_path)

if __name__ == '__main__':
    unittest.main()


"""
Issues:
When trying to test the index_creation function, I encounter an issue with 
the file path for the json index files. They are created at a different location.
Is there any way to make the location of these index files not relative to the 
path of the python file from where they are created?

Question:
What is the tearDown method for? E.g. should I move the deletion of the temp files
there?

"""