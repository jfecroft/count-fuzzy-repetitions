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
from itertools import izip, tee, islice

ARGUMENTS = docopt(__doc__, version='parse text 1.0')

def nwise(iterable, n=2):
    iters = tee(iterable, n)
    for i, it in enumerate(iters):
        next(islice(it, i, i), None)
    return izip(*iters)


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
        for word in nwise(line.split(), n=INPUT_DICT['n']):
            word = ' '.join(word)
            if INPUT_DICT['strip']:
                word = word.strip("',.;:?!").title()
            WORDS_USED[word].append('{}.{}'.format(i+1, line_num+1))

with open('repititions_{}pairs.dat'.format(INPUT_DICT['n']), 'w') as f:
    f.write('phrase, times used, lines used\n')
    for key, value in sorted(WORDS_USED.iteritems()):
        if len(value) > INPUT_DICT['min_reps']:
            f.write('"{}", {}, {}\n'.format(key, len(value), value))
