"""
Returns the frequency of words in *FILE_NAME*'.txt' and the lines on which they
are used. the data is written to *FILE_NAME*'.dat'
"""
import sys

from collections import defaultdict

FILE_NAME = sys.argv[1]

with open(FILE_NAME+'.txt') as f:
    content = f.readlines()

lines_used = defaultdict(list)
for line_num, line in enumerate(content):
    for word in line.split():
        lines_used[word].append(line_num)

with open(FILE_NAME+'.dat', 'w') as f:
    for key, value in sorted(lines_used.items()):
        f.write('{}, {}, {} \n'.format(key, len(value), value))
