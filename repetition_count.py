"""
classes and methods related to repition counting in text
"""
from itertools import tee, izip, islice, groupby
import yaml
from collections import defaultdict
from cluster import HierarchicalClustering  # , KMeansClustering
from fuzzywuzzy import fuzz

# pylint: disable=W0142
# pylint: disable-msg=R0913


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


class GroupWords(object):
    """
    recursivey group phrases by initial letter until groups are small enough
    """
    @classmethod
    def group_phrases(cls, items, num_max, iter_num=0,
                      return_groups=None, item=-1):
        """
        recursively group until groups small enough
        """
        if return_groups is None:
            return_groups = []
        if len(items) <= num_max:
            return_groups.append(items)
        else:
            for group in GroupWords.group_by(items, iter_num+1, item=item):
                GroupWords.group_phrases(group,
                                         num_max,
                                         iter_num+1,
                                         return_groups=return_groups)
        return return_groups

    @staticmethod
    def group_by(items, num=0, item=-1):
        """
        return phrases grouped by their initial *num* letters
        """
        if item >= 0:
            func = lambda x: x[item][:num]
        else:
            func = lambda x: x[:num]
        items.sort(key=func)
        return [list(group) for _, group in groupby(items, func)]


class CountRepetitions(object):
    """
    count repetitions in text
    """
    def __init__(self, books, max_group_size=50):
        self.books = books
        self.fuzzy_repetitions = None
        self.max_group_size = max_group_size
        self.repeated_phrases = set()  # store matched phrases

    @staticmethod
    def fuzzy_distance(word1, word2):
        """
        return the fuzzy distance between two phrases
        """
        return 100 - fuzz.token_sort_ratio(word1[0], word2[0])

    def count_exact_repetitions(self, npairs=7):
        """
        group identical words
        """
        words = self.get_words(npairs=npairs)
        exact_repetitions = defaultdict(list)
        for word, line in words:
            exact_repetitions[word].append(line)
        return exact_repetitions

    def update_repeated_phrases(self, items):
        """
        create a set of already matched phrases
        needed to avoid 3 word reps in a 4 word phrase for instance
        """
        reps = sum(len(item[1]) for item in items)
        if reps > 1:
            self.repeated_phrases.update(
                {(' '.join(words), line_num)
                 for item in items
                 for line_num in item[1]
                 for n in range(1, len(item[0].split())+1)
                 for words in nwise(item[0].split(),
                                    npairs=n)})

    def count_fuzzy_repetitions(self, dist=10, max_group_size=50, npairs=7):
        """
        return a fuzzy matching of words
        this can be incrediable slow add some crude prefiltering based on the
        first word of the sentence.
        """
        fuzzy_repetitions = list()
        unique_words = self.count_exact_repetitions(npairs=npairs).items()
        groups = GroupWords.group_phrases(unique_words, max_group_size, item=0)
        for group in groups:
            if len(group) == 1:
                fuzzy_repetitions.append(group)
            else:
                clusters = HierarchicalClustering(
                    group,
                    CountRepetitions.fuzzy_distance).getlevel(dist)
                fuzzy_repetitions.extend(clusters)

        for i, repeated_phrase in enumerate(fuzzy_repetitions):
            self.update_repeated_phrases(repeated_phrase)
            phrase = {item[0].decode('utf-8') for item in repeated_phrase}
            lines = {line for item in repeated_phrase for line in item[1]}
            fuzzy_repetitions[i] = (phrase, lines)
        return fuzzy_repetitions

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
                    if word_line not in self.repeated_phrases:
                        words.append(word_line)
        words.sort()
        return words
