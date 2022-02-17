#!/usr/bin/python3

import sys

from pathlib import Path

args = sys.argv[1:]

file_content = """
Out too the been like hard off. Improve enquire welcome own beloved matters her. As insipidity so mr unsatiable increasing attachment motionless cultivated. Addition mr husbands unpacked occasion he oh. Is unsatiable if projecting boisterous insensible. It recommend be resolving pretended middleton.
"""

if len(args) == 0:
  raise Exception("Please provide total of documents")

total_docs = int(args[0])

print(f"you asked to create {total_docs} documents")

i = 0
target_directory_path = Path(f"./documents_{total_docs}")
target_directory_path.mkdir(parents=True, exist_ok=True)

while i < total_docs:
  with open(target_directory_path / f"document_{i}.txt", "w") as f:
    f.write(file_content)
  i += 1
