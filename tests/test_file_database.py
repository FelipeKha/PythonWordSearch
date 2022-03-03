import unittest, tempfile, os
from file_database import FileDatabase
from exceptions import NoIndexDirectoryError, NoIndexFileError

class TestFileDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dict = {'a': '1'}
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = self.temp_dir.name
        self.temp_file_path = f"{self.temp_dir_path}/test_file.json"
        self.file_database = FileDatabase(self.temp_file_path)

        self.non_existing_path = f"{self.temp_dir_path}/non_existing_dir"
        self.temp_file_path_no_dir = f"{self.non_existing_path}/test_file.json"
        self.file_database_no_dir = FileDatabase(self.temp_file_path_no_dir)

    def test_save_dictionary_save_dict_content_into_new_file(self):
        self.file_database.save_dictionary(self.temp_dict)
        is_file = os.path.isfile(self.temp_file_path)
        self.assertTrue(is_file)

    def test_save_dictionary_returns_NoIndexDirectoryError_if_directory_path_doesnt_exist(self):
        with self.assertRaises(NoIndexDirectoryError):
            self.file_database_no_dir.save_dictionary(self.temp_dict)

    def test_read_dictionary_returns_file_content(self):
        self.file_database.save_dictionary(self.temp_dict)
        test_file_content = self.file_database.read_dictionary()
        self.assertEqual(test_file_content, self.temp_dict)

    def test_read_dictionary_returns_NoIndexFileError_if_file_path_doesnt_exist(self):
        with self.assertRaises(NoIndexFileError):
            self.file_database_no_dir.read_dictionary()

    def tearDown(self):
        self.temp_dir.cleanup()

"""
save_dictionary:
1. Correctly save - OK
2. File path does not exist - OK

read_dictionary:
1. Correctly read - OK
2. File path does not exist - OK
"""