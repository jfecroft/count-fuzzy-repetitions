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


def load_yaml(filen):
    """
    load a yaml file and return the json object
    """
    with open('{}.yml'.format(filen), 'r') as open_file:
        return_dict = yaml.load(open_file)
    return return_dict

LATIN_SUFFIXES = load_yaml('suffix')
LATIN_SUFFIXES = [suffix for
                  values in LATIN_SUFFIXES.values() for
                  suffix in values]
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
        if len(value) > 1:
            f.write('{}, {}, {}\n'.format(key, len(value), value))
