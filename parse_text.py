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


def main():
    """
    run from command line
    """
    arguments = docopt(__doc__, version='parse text 1.0')
    input_dict = load_yaml(arguments['--input'])
    books = input_dict['books']
    max_word_phrases = input_dict['max_word_phrases']
    min_word_phrases = input_dict['min_word_phrases']
    min_reps = input_dict['min_reps']
    fuzzy_dist = input_dict['fuzzy_dist']
    max_group_size = input_dict['max_group_size']
    dist_func = input_dict['dist_func']

    luc = CountRepetitions(books=books)
    fuzzy_repetitions = []
    for i in range(max_word_phrases, min_word_phrases-1, -1):
        print 'Processing {} words phrases'.format(i)
        repetitions = luc.count_fuzzy_repetitions(
            dist=fuzzy_dist,
            max_group_size=max_group_size,
            npairs=i,
            dist_func=dist_func)
        print 'Found {} repetitions of {} word phrases'.format(
            len(repetitions), i)
        fuzzy_repetitions.extend(repetitions)

    filen = '{}_repetitions.dat'.format(arguments['--input'])
    fuzzy_repetitions.sort(key=lambda x: len(x[1]), reverse=True)
    with open(filen, 'w') as open_file:
        open_file.write('phrase, times used, lines used\n')
        for words, lines in fuzzy_repetitions:
            if len(lines) > min_reps:
                open_file.write('{}, {}, {}\n'.format(
                    "['{}']".format("', '".join(words)),
                    len(lines),
                    '[{}]'.format(', '.join(lines))))
if __name__ == '__main__':
    main()
