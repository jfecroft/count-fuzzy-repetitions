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
from fuzzywuzzy import fuzz

ARGUMENTS = docopt(__doc__, version='parse text 1.0')


def load_yaml(filen):
    with open('{}.yml'.format(filen), 'r') as f:
        RETURN_DICT = yaml.load(f)
    return RETURN_DICT

INPUT_DICT = load_yaml(ARGUMENTS['<input>'])
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
    for key, value in sorted(WORDS_USED.iteritems()):
        f.write('{}, {}, {}\n'.format(key, len(value), value))
