#!../virtual/bin/python3

from backend import Index, Search
import click

@click.command()
@click.option('--search_folder', prompt='Enter folder to search', help='Name of the folder to be searched')
@click.option('--search_word', prompt='Enter word to search', help='Word to be searched in selected folder')
@click.option('--capitalization_matter', prompt='Does capitalization matter?', help='Specify if the capitalization of the word entered for search matter', is_flag=True)



def search(search_folder, search_word, capitalization_matter):
    index = Index(search_folder)
    search = Search(search_word, index._index_file_path, index._index_no_cap_file_path)

    indexation_required = index.indexation_required()
    print(f"Indexation required: {indexation_required}")

    if indexation_required:
        index.index_creation()

    if capitalization_matter:
        print(search.search_cap())
    else:
        print(search.search_no_cap())


if __name__ == '__main__':
    search()


"""
Function or class required after a decorator, why?
List comprehension on row 82 of backend.py does not work, need to figure out why (this leads to repeating results)
Indexation is too slow, how can we speed it up?
"""

