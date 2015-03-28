"""
classes and methods related to repition counting in text
"""
from itertools import tee, izip, islice
import yaml
from collections import defaultdict


def nwise(iterable, npairs=2):
    """
    return a iterator which return consecutive npairs
    """
    iters = tee(iterable, npairs)
    for i, iterator in enumerate(iters):
        next(islice(iterator, i, i), None)
    return izip(*iters)


def load_yaml(filen):
    """
    load a yaml file and return the json object
    """
    with open('{}.yml'.format(filen), 'r') as open_file:
        return_dict = yaml.load(open_file)
    return return_dict


class CountRepetitions(object):
    """
    class to count repetitions in text
    """
    def __init__(self, books, npairs=1, strip=False, *args, **kwargs):
        # init the words of interest
        self.words = None
        self.get_words(books, npairs, strip)
        self.repetitions = None

    def get_identical_words(self):
        """
        group identical words
        """
        words_used = defaultdict(list)
        for word, line in self.words:
            words_used[word].append(line)
        self.repetitions = words_used

    def get_words(self, books, npairs=1, strip=False):
        """
        return a list of tuples of the form (word, line)
        """
        words = []
        for i, book in enumerate(books):
            with open(book+'.txt') as open_file:
                content = open_file.readlines()

            for line_num, line in enumerate(content):
                for word in nwise(line.split(), npairs=npairs):
                    word = ' '.join(word)
                    if strip:
                        word = word.strip("',.;:?!").title()
                    words.append((word, '{}.{}'.format(i+1, line_num+1)))
        self.words = words

    def write_repetitions(self, filen='out.dat', min_reps=0):
        """
        write repetitions to file
        """
        with open(filen, 'w') as open_file:
            open_file.write('phrase, times used, lines used\n')
            for key, value in sorted(self.repetitions.iteritems()):
                if len(value) > min_reps:
                    open_file.write('"{}", {}, {}\n'.format(key,
                                                            len(value),
                                                            value))


def strip_suffix(word, suffixes):
    """
    return the root of the word without suffix
    """
    for suffix in suffixes:
        if word.endswith(suffix):
            word = word.rstrip(suffix)
            return word
    print word, 'couldnt remove suffix'
    return 'ZZZZ'  # return something more sensible
