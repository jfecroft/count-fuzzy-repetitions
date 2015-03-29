"""
classes and methods related to repition counting in text
"""
from itertools import tee, izip, islice, groupby
import yaml
from collections import defaultdict
from cluster import HierarchicalClustering  # , KMeansClustering
from fuzzywuzzy import fuzz


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


def fuzzy_distance(x, y):
    return 100 - fuzz.token_sort_ratio(x[0], y[0])


def match_first_word(x, y):
    if x.split()[0] == y.split()[0]:
        return 0
    else:
        return 1


def groupby_first_letter(items, func=lambda x: x[0]):
    items.sort(key=func)
    return [list(group) for key, group in groupby(items, func)]


class CountRepetitions(object):
    """
    count repetitions in text
    """
    def __init__(self, books, npairs=1, strip=False, *args, **kwargs):
        # init the words of interest
        self.strip = strip
        self.npairs = npairs
        self.books = books
        self.words = self.get_words()
        self.exact_repetitions = defaultdict(list)
        self.fuzzy_repetitions = list()

    def get_exact_repetitions(self):
        """
        group identical words
        """
        for word, line in self.words:
            self.exact_repetitions[word].append(line)

    def get_fuzzy_repetitions(self, dist=10, group_letters=2):
        """
        return a fuzzy matching of words
        this can be incrediable slow add some crude prefiltering based on the
        first word of the sentence.
        """
        unique_words = self.exact_repetitions.items()
        #unique_words = unique_words[:100]
        groups = groupby_first_letter(unique_words, func=lambda x: x[0][:group_letters])
        for group in groups:
            print 'comparing words starting {}'.format(group[0][0][:group_letters])
            print 'there are {}'.format(len(group))
            clusters = HierarchicalClustering(
                group,
                fuzzy_distance)
            cluster = clusters.getlevel(dist)
            if len(cluster) > 1: 
                self.fuzzy_repetitions.extend(cluster)
            else:
                self.fuzzy_repetitions.append(cluster)
        # convert to standard form
        tmp = []
        for i in self.fuzzy_repetitions:
            words = {item[0] for item in i}
            lines = {line for item in i for line in item[1]}
            tmp.append((words, lines))
        self.fuzzy_repetitions = tmp

    def get_words(self):
        """
        return a list of tuples of the form (word, line)
        """
        words = []
        for i, book in enumerate(self.books):
            with open(book+'.txt') as open_file:
                content = open_file.readlines()
            for line_num, line in enumerate(content):
                for word in nwise(line.split(), npairs=self.npairs):
                    word = ' '.join(word)
                    if self.strip:
                        word = word.strip("',.;:?!").title()
                    words.append((word, '{}.{}'.format(i+1, line_num+1)))
        words.sort()
        return words

    def write_exact_repetitions(self, filen='out.dat', min_reps=0):
        """
        write repetitions to file
        """
        with open(filen, 'w') as open_file:
            open_file.write('phrase, times used, lines used\n')
            for key, value in sorted(self.exact_repetitions.iteritems()):
                if len(value) > min_reps:
                    open_file.write('"{}", {}, {}\n'.format(key,
                                                            len(value),
                                                            value))

    def write_fuzzy_repetitions(self, filen='fuzzy.dat', min_reps=0):
        """
        write repetitions to file
        """
        with open(filen, 'w') as open_file:
            open_file.write('phrase, times used, lines used\n')
            for words, lines in self.fuzzy_repetitions:
                if len(lines) > min_reps:
                    open_file.write('{}, {}, {}\n'.format(list(words),
                                                          len(lines),
                                                          list(lines)))


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
