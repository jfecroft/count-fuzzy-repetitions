#! /usr/bin/env python
"""
Usage:
  parse_text.py [--input=<input>]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --input=<input>       Input yml file [default: lucretius]
"""
from docopt import docopt
from repetition_count import (
    CountRepetitions,
    load_yaml,
    )

ARGUMENTS = docopt(__doc__, version='parse text 1.0')
INPUT_DICT = load_yaml(ARGUMENTS['--input'])
BOOKS = INPUT_DICT['books']
NPAIRS = INPUT_DICT['npairs']
MIN_REPS = INPUT_DICT['min_reps']
STRIP = INPUT_DICT['strip']
FUZZY_DIST = INPUT_DICT['fuzzy_dist']
MAX_GROUP_SIZE = INPUT_DICT['max_group_size']
MIN_FUZZY_REPS = INPUT_DICT['min_fuzzy_reps']


LUC = CountRepetitions(books=BOOKS)
FUZZY_REPETITIONS = []
for i in range(10, 1, -1):
    repetitions = LUC.count_fuzzy_repetitions(
        dist=FUZZY_DIST,
        max_group_size=MAX_GROUP_SIZE,
        npairs=i)
    FUZZY_REPETITIONS.extend(repetitions)

FILEN = '{}_repetitions.dat'.format(ARGUMENTS['--input'])
FUZZY_REPETITIONS.sort(key=lambda x: len(x[1]), reverse=True)
with open(FILEN, 'w') as open_file:
    open_file.write('phrase, times used, lines used\n')
    for words, lines in FUZZY_REPETITIONS:
        if len(lines) > MIN_REPS and len(words) > MIN_FUZZY_REPS:
            open_file.write('{}, {}, {}\n'.format(list(words),
                                                  len(lines),
                                                  list(lines)))
