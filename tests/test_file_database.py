import os
import shutil
import tempfile
import unittest

from demo.backend import FileDatabase, DictionaryNotSavedException


class TestFileDatabase(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_when_save_then_file_is_created(self):
        # given
        file_path = f"{self.test_dir}/example_file.json"
        database = FileDatabase(db_file_path=file_path)

        # when
        dict_to_save = {"lala": "hey"}
        database.save_dictionary(dict_to_save)

        # then
        self.assertTrue(os.path.isfile(file_path))
        # assert that file content is xxx

    def test_given_directory_path_does_not_exist_when_save_then_raises_specific_error(self):
        # TODO
        self.fail("implement me")

    def test_given_directory_path_does_not_exist_when_save_then_raises_specific_error(self):
        # TODO
        self.fail("implement me")

    def test_given_file_when_read_then_return_file_content_as_dictionary(self):
        # given
        file_path = f"{self.test_dir}/example_file.json"
        database = FileDatabase(db_file_path=file_path)
        # and
        dict_to_save = {"lala": "hey"}
        database.save_dictionary(dict_to_save)

        # when
        dict_loaded = database.read_dictionary()

        # then
        self.assertEqual(dict_loaded, dict_to_save)

    def test_given_file_does_not_exist_when_read_then_raises_specific_error(self):
        # given
        file_path = f"lalalalalala/example_file.json"
        database = FileDatabase(db_file_path=file_path)

        # when / then
        try:
            database.read_dictionary()
        except DictionaryNotSavedException as e:
            self.assertTrue(e is not None)

