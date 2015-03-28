#! /usr/bin/env python
"""
Usage:
  parse_text.py input <input>

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt
from rep_funcs import (
    CountRepititions,
    load_yaml,
    )

ARGUMENTS = docopt(__doc__, version='parse text 1.0')
INPUT_DICT = load_yaml(ARGUMENTS['<input>'])
BOOKS = INPUT_DICT['books']

#luc = CountRepititions(BOOKS, npairs=INPUT_DICT['n'], strip=INPUT_DICT['strip'])
luc = CountRepititions(**INPUT_DICT)
luc.get_identical_words()
luc.write_repititions(filen='repititions_{}pairs.dat'.format(INPUT_DICT['npairs']),
                      min_reps=INPUT_DICT['min_reps'])
