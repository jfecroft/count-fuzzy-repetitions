"""
Usage:
  parse_text.py books <books>...

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt
from collections import defaultdict


ARGUMENTS = docopt(__doc__, version='parse text 1.0')

BOOKS = ARGUMENTS['<books>']

LINES_USED = defaultdict(list)
for i, book in enumerate(BOOKS):
    with open(book+'.txt') as f:
        CONTENT = f.readlines()

    for line_num, line in enumerate(CONTENT):
        for word in line.split():
            word = word.rstrip(',.;:').title()
            LINES_USED[word].append('{}.{}'.format(i+1, line_num))

with open('out.dat', 'w') as f:
    for key, value in sorted(LINES_USED.items()):
        f.write('{}, {}, {} \n'.format(key, len(value), value))
