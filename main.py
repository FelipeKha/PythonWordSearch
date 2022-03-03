#!../virtual/bin/python3

import os
from index_management import IndexManagement
from search import Search
from file_database import FileDatabase
from indexation_multi_process_queue_full_txt import Indexation
import click
import time

# @click.command()
# @click.option('--search_folder', prompt='Enter folder to search', help='Name of the folder to be searched')
# @click.option('--search_word', prompt='Enter word to search', help='Word to be searched in selected folder')
# @click.option('--capitalization_matter', prompt='Does capitalization matter?', help='Specify if the capitalization of the word entered for search matter', is_flag=True)
#
#
#
# def search(search_folder, search_word, capitalization_matter):
#
#     current_path = os.path.abspath(os.path.dirname(__file__))
#     search_folder_path = f"{current_path}/text_documents/{search_folder}"
#     index_file_path_upper = f"{current_path}/index_files/index_{search_folder}_upper.json"
#     index_file_path_lower = f"{current_path}/index_files/index_{search_folder}_lower.json"
#
#
#     file_database_upper = FileDatabase(index_file_path_upper)
#     file_database_lower = FileDatabase(index_file_path_lower)
#
#     index_management = IndexManagement(search_folder_path, file_database_upper, file_database_lower)
#
#     search = Search(search_word, file_database_upper.index_file_path, file_database_lower.index_file_path)
#
#     indexation_required = index_management.indexation_required()
#     print(f"Indexation required: {indexation_required}")
#
#     if indexation_required:
#         print("Indexation started")
#         t0 = process_time()
#         indexation = Indexation(index_management.text_file_paths_list)
#         index_dict = indexation.indexation()
#         t1 = process_time()
#         indexation_time = t1-t0
#         index_management.jsons_creation(index_dict, indexation_time)
#         print("Indexation ended")
#         print(f"Indexation took {file_database_upper.read_indexation_time()} seconds, and building of lower index {file_database_lower.read_indexation_time()} seconds")
#
#     if capitalization_matter:
#         print(search.search_cap())
#     else:
#         print(search.search_no_cap())


if __name__ == '__main__':
    # search()

    current_path = os.path.abspath(os.path.dirname(__file__))

    while True:
        search_folder = input('Enter folder to search: ')
        search_folder_path = f"{current_path}/text_documents/{search_folder}"

        if os.path.isdir(search_folder_path):
            break

        else:
            print(f"There is no folder '{search_folder}', please enter existing folder")

    search_word = input('Enter word to search: ')

    while True:
        capitalization_matter_input = input('Does capitalization matter? [y/N]: ')
        if (capitalization_matter_input == 'y' or capitalization_matter_input == 'N'):
            capitalization_matter = capitalization_matter_input == 'y'
            break
        else:
            print(f"'{capitalization_matter_input}' is not a valid input, please enter 'y' or 'N'")

    index_file_path_upper = f"{current_path}/index_files/index_{search_folder}_upper.json"
    index_file_path_lower = f"{current_path}/index_files/index_{search_folder}_lower.json"

    file_database_upper = FileDatabase(index_file_path_upper)
    file_database_lower = FileDatabase(index_file_path_lower)

    index_management = IndexManagement(search_folder_path, file_database_upper,
                                       file_database_lower)

    search = Search(search_word, file_database_upper, file_database_lower)

    indexation_required = index_management.indexation_required()
    print(f"Indexation required: {indexation_required}")

    if indexation_required:
        print("Indexation started")
        t0 = time.time()
        indexation = Indexation(index_management.text_file_paths_list)
        index_dict = indexation.indexation()
        t1 = time.time()
        indexation_time = t1-t0
        index_management.jsons_creation(index_dict, indexation_time)
        print("Indexation ended")
        print(f"Indexation took {file_database_upper.read_indexation_time()} seconds, and building of lower index {file_database_lower.read_indexation_time()} seconds")

    if capitalization_matter:
        print(search.search_upper())
    else:
        print(search.search_lower())

"""
- Function or class required after a decorator, why?
- How can I improve presentation to remain within the 80 character per row rule?
- Can we walk through the order of execution of indexation_multi_process_queue.py?
- I am not sure the test for error raised work currenly, it seems that it raises 
an error instead of saying failed test
- Should we implement the continuous indexing, or do that with another program?
"""

