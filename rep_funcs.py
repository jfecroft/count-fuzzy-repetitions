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


def group_by(items, n=0):
    func = lambda x: x[0][:n]
    items.sort(key=func)
    return [list(group) for key, group in groupby(items, func)]


def rec_group(items, n, ii=0, return_groups=None):
    if return_groups is None:
        return_groups = []
    if len(items) <= n:
        return_groups.append(items)
    else:
        for group in group_by(items, ii+1):
            rec_group(group, n, ii+1, return_groups=return_groups)
    return return_groups


def groupby_first_letter(items, func=lambda x: x[0]):
    items.sort(key=func)
    return [list(group) for key, group in groupby(items, func)]


class CountRepetitions(object):
    """
    count repetitions in text
    """
    def __init__(self, books, max_group_size=50):
        # init the words of interest
        # self.strip = strip
        # self.npairs = npairs
        self.books = books
        # self.words = self.get_words()
        self.fuzzy_repetitions = None
        self.max_group_size = max_group_size
        self.matched = set()  # store matched phrases

    def get_exact_repetitions(self, npairs=7):
        """
        group identical words
        """
        words = self.get_words(npairs=npairs)
        exact_repetitions = defaultdict(list)
        for word, line in words:
            exact_repetitions[word].append(line)
        return exact_repetitions

    def add_all_to_set(self, items):
        """
        create a set of already matched phrases
        needed to avoid 3 word reps in a 4 word phrase for instance
        """
        reps = sum(len(item[1]) for item in items)
        if reps > 1:
            print items, reps
            for item in items:
                for line_num in item[1]:
                    for n in range(1, len(item[0].split())+1):
                        for words in nwise(item[0].split(), npairs=n):
                            word = ' '.join(words)
                            self.matched.update([(word, line_num)])

    def get_fuzzy_repetitions(self, dist=10, max_group_size=50, npairs=7):
        """
        return a fuzzy matching of words
        this can be incrediable slow add some crude prefiltering based on the
        first word of the sentence.
        """
        self.fuzzy_repetitions = list()
        unique_words = self.get_exact_repetitions(npairs=npairs).items()
        # recursive group need testing.
        groups = rec_group(unique_words, max_group_size)
        for group in groups:
            if len(group) == 1:
                self.fuzzy_repetitions.append(group)
            else:
                clusters = HierarchicalClustering(
                    group,
                    fuzzy_distance).getlevel(dist)
                self.fuzzy_repetitions.extend(clusters)
        tmp = []
        for i in self.fuzzy_repetitions:
            self.add_all_to_set(i)
            words = {item[0] for item in i}
            lines = {line for item in i for line in item[1]}
            tmp.append((words, lines))
        return tmp

    def get_words(self, npairs):
        """
        return a list of tuples of the form (word, line)
        """
        words = []
        for i, book in enumerate(self.books):
            with open(book+'.txt') as open_file:
                content = open_file.readlines()
            for line_num, line in enumerate(content):
                for word in nwise(line.split(), npairs=npairs):
                    word = ' '.join(word)
                    word_line = (word, '{}.{}'.format(i+1, line_num+1))
                    if word_line not in self.matched:
                        words.append(word_line)
                    else:
                        pass
        words.sort()
        return words


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
