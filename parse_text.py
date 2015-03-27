#! /usr/bin/env python
"""
Usage:
  parse_text.py input <input>

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt
from collections import defaultdict
import yaml


ARGUMENTS = docopt(__doc__, version='parse text 1.0')

with open('{}.yml'.format(ARGUMENTS['<input>']), 'r') as f:
    INPUT_DICT = yaml.load(f)

BOOKS = INPUT_DICT['books']
WORDS_USED = defaultdict(list)

for i, book in enumerate(BOOKS):
    with open(book+'.txt') as f:
        CONTENT = f.readlines()

    for line_num, line in enumerate(CONTENT):
        for word in line.split():
            word = word.strip("',.;:?!").title()
            if word.isalpha() is False:
                print word
            WORDS_USED[word].append('{}.{}'.format(i+1, line_num+1))

with open('out.dat', 'w') as f:
    f.write('word, times used, lines used\n')
    for key, value in sorted(WORDS_USED.items()):
        f.write('{}, {}, {}\n'.format(key, len(value), value))
