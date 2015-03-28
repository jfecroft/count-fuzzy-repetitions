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
    CountRepetitions,
    load_yaml,
    )

ARGUMENTS = docopt(__doc__, version='parse text 1.0')
INPUT_DICT = load_yaml(ARGUMENTS['<input>'])
BOOKS = INPUT_DICT['books']
NPAIRS = INPUT_DICT['npairs']
MIN_REPS = INPUT_DICT['min_reps']


LUC = CountRepetitions(books=BOOKS, npairs=NPAIRS, min_reps=MIN_REPS)
LUC.get_identical_words()
LUC.write_repetitions(
    filen='repetitions_{}pairs.dat'.format(INPUT_DICT['npairs']),
    min_reps=INPUT_DICT['min_reps'])
