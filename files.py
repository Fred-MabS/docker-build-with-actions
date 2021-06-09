import os
import re

all_files = os.walk('.')
file_contains_regex = 'Dockerfile(.*)'
for _, _, filenames in all_files:
    file_contains_regex_object = re.compile(file_contains_regex, flags=re.MULTILINE)
    for filename in filenames:
        if file_contains_regex_object.search(filename):
            print(f'{filename}')
