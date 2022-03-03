import unittest
from search import Search

class ArtificialFileDatabaseUpper:

    def __init__(self, word_searched_upper, word_searched_lower,
                 test_result_upper, test_result_lower):
        self.word_searched_upper = word_searched_upper
        self.word_searched_lower = word_searched_lower
        self.test_result_upper = test_result_upper
        self.test_result_lower = test_result_lower

    def read_dictionary(self):
        index = {'index': {self.word_searched_upper: [self.test_result_upper],
                           self.word_searched_lower: [self.test_result_lower]}}
        return index

class ArtificialFileDatabaseLower:

    def __init__(self, word_searched_upper, word_searched_lower,
                 test_result_upper, test_result_lower):
        self.word_searched_upper = word_searched_upper
        self.word_searched_lower = word_searched_lower
        self.test_result_upper = test_result_upper
        self.test_result_lower = test_result_lower

    def read_dictionary(self):
        index = {'index': {self.word_searched_lower: [self.test_result_upper, self.test_result_lower]}}
        return index

class TestSearch(unittest.TestCase):

    def setUp(self):
        self.word_searched_upper = "Test"
        self.test_result_upper = "test_result_upper"
        self.word_searched_lower = "test"
        self.test_result_lower = "test_result_lower"
        self.word_searched_no_result = "No_word"
        self.artificial_file_database_upper = ArtificialFileDatabaseUpper(self.word_searched_upper,
                                                                          self.word_searched_lower,
                                                                          self.test_result_upper,
                                                                          self.test_result_lower)
        self.artificial_file_database_lower = ArtificialFileDatabaseLower(self.word_searched_upper,
                                                                          self.word_searched_lower,
                                                                          self.test_result_upper,
                                                                          self.test_result_lower)
        self.search_upper = Search(self.word_searched_upper, self.artificial_file_database_upper,
                             self.artificial_file_database_lower)
        self.search_lower = Search(self.word_searched_lower, self.artificial_file_database_upper,
                             self.artificial_file_database_lower)
        self.search_no_result = Search(self.word_searched_no_result, self.artificial_file_database_upper,
                             self.artificial_file_database_lower)

    def test_search_upper_returns_expected_result(self):
        self.assertEqual([self.test_result_upper],
                         self.search_upper.search_upper())

    def test_search_lower_returns_expected_result(self):
        self.assertEqual([self.test_result_upper, self.test_result_lower],
                         self.search_upper.search_lower())

    def test_search_upper_returns_empty_list_when_no_result(self):
        self.assertEqual([], self.search_no_result.search_upper())

    def test_search_lower_returns_empty_list_when_no_result(self):
        self.assertEqual([], self.search_no_result.search_lower())

    def test_search_lower_returns_results_for_search_upper_with_the_same_upper_and_lower_word(self):
        self.assertEqual([self.search_upper.search_upper()[0], self.search_lower.search_upper()[0]],
                         self.search_upper.search_lower())



"""
search_upper, search_lower:
1. Returns expected result
2. Returns empty list when no result

search_lower:
1. Returns the results for search_upper "is" and "Is"
"""