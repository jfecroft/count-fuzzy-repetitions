#! /usr/bin/env python
"""
Usage:
  parse_text.py [--input=<input>]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --input=<input>       Input yml file [default: lucretius]
"""
# pylint: disable=F0401
from docopt import docopt
# pylint: enable=F0401
from repetition_count import (
    CountRepetitions,
    load_yaml,
    )


ARGUMENTS = docopt(__doc__, version='parse text 1.0')
INPUT_DICT = load_yaml(ARGUMENTS['--input'])
BOOKS = INPUT_DICT['books']
MAX_WORD_PHRASES = INPUT_DICT['max_word_phrases']
MIN_WORD_PHRASES = INPUT_DICT['min_word_phrases']
MIN_REPS = INPUT_DICT['min_reps']
FUZZY_DIST = INPUT_DICT['fuzzy_dist']
MAX_GROUP_SIZE = INPUT_DICT['max_group_size']

# TODO pdf output

LUC = CountRepetitions(books=BOOKS)
FUZZY_REPETITIONS = []
for i in range(MAX_WORD_PHRASES, MIN_WORD_PHRASES-1, -1):
    print 'Processing {} words phrases'.format(i)
    repetitions = LUC.count_fuzzy_repetitions(
        dist=FUZZY_DIST,
        max_group_size=MAX_GROUP_SIZE,
        npairs=i)
    print 'Found {} repetitions of {} word phrases'.format(len(repetitions), i)
    FUZZY_REPETITIONS.extend(repetitions)

FILEN = '{}_repetitions.dat'.format(ARGUMENTS['--input'])
FUZZY_REPETITIONS.sort(key=lambda x: len(x[1]), reverse=True)
with open(FILEN, 'w') as open_file:
    open_file.write('phrase, times used, lines used\n')
    for words, lines in FUZZY_REPETITIONS:
        if len(lines) > MIN_REPS:
            open_file.write('{}, {}, {}\n'.format(
                "['{}']".format("', '".join(words)),
                len(lines),
                '[{}]'.format(', '.join(lines))))
