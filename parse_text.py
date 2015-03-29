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
STRIP = INPUT_DICT['strip']
FUZZY_DIST = INPUT_DICT['fuzzy_dist']
GROUP_LETTERS = INPUT_DICT['group_letters']


LUC = CountRepetitions(books=BOOKS,
                       npairs=NPAIRS,
                       min_reps=MIN_REPS,
                       strip=STRIP)
LUC.get_exact_repetitions()
LUC.get_fuzzy_repetitions(dist=FUZZY_DIST)


LUC.write_exact_repetitions(
    filen='repetitions_{}pairs.dat'.format(INPUT_DICT['npairs']),
    min_reps=INPUT_DICT['min_reps'])
LUC.write_fuzzy_repetitions(min_reps=INPUT_DICT['min_reps'])
