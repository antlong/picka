from warnings import warn
from functools import wraps
from os.path import join, dirname
from random import choice, randint
from string import ascii_uppercase, ascii_letters, ascii_lowercase, punctuation
from re import split, compile
from itertools import izip
from functools import partial
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import class_mapper

__docformat__ = 'restructuredtext en'

path = os.path.join(os.path.dirname(
    __file__) + "/data/db.sqlite")


def engine_connection():
    return create_engine("sqlite:///" + path, echo=False)


def asdict(obj):
    return dict((col.name, getattr(obj, col.name))
                for col in class_mapper(obj.__class__).mapped_table.c)


def deprecated(replacement=None):
    def outer(fun):
        msg = "picka.%s is deprecated" % fun.__name__
        if replacement is not None:
            msg += "; use %s instead" % replacement
        if fun.__doc__ is None:
            fun.__doc__ = msg

        @wraps(fun)
        def inner(*args, **kwargs):
            warn(msg, category=DeprecationWarning, stacklevel=2)
            return fun(*args, **kwargs)

        return inner

    return outer


def ssn_prefixes(state):
    states = {
        "AL": [[416, 424]],
        "AK": [[574, 574]],
        "AR": [[429, 432], [676, 679]],
        "AZ": [[526, 527], [600, 601]],
        "CA": [[1, 7], [545, 573], [602, 626]],
        "CO": [[521, 524], [650, 653]],
        "CT": [[40, 49]],
        "DE": [[221, 222]],
        "FL": [[261, 267], [589, 595], [766, 772]],
        "GA": [[252, 260], [667, 675]],
        "HI": [[575, 576], [750, 751]],
        "ID": [[518, 519]],
        "IL": [[318, 361]],
        "IN": [[303, 317]],
        "IA": [[478, 485]],
        "KS": [[509, 515]],
        "KY": [[400, 407]],
        "LA": [[433, 439], [659, 665]],
        "ME": [[4, 7]],
        "MD": [[212, 220]],
        "MA": [[10, 34]],
        "MI": [[362, 386]],
        "MN": [[468, 477]],
        "MS": [[425, 428], [587, 588], [752, 755]],
        "MO": [[468, 500]],
        "MT": [[516, 517]],
        "NE": [[505, 508]],
        "NV": [[530, 680]],
        "NH": [[1, 3]],
        "NJ": [[135, 158]],
        "NM": [[525, 585], [648, 649]],
        "NY": [[50, 134]],
        "NC": [[237, 246], [681, 690]],
        "ND": [[501, 501]],
        "OH": [[268, 302]],
        "OK": [[440, 448]],
        "OR": [[540, 544]],
        "PA": [[159, 211]],
        "RI": [[035, 39]],
        "SC": [[247, 251], [654, 658]],
        "SD": [[504, 504]],
        "TN": [[408, 415], [756, 763]],
        "TX": [[449, 467], [627, 645]],
        "UT": [[528, 529], [646, 647]],
        "VT": [[8, 9]],
        "VI": [[223, 231], [232, 236]],
        "WA": [[531, 539]],
        "WV": [[232, 236]],
        "WI": [[387, 399]],
        "WY": [[520, 520]]
    }
    return states[state]


def random_string(length=1, case='upper'):
    """
    This will allow you to enter an integer, and create 'i' amount
    of characters. ie: random_string(7) = DsEIzCd
    """
    choices = ''
    output = ''
    cases = {
        'upper': ascii_uppercase,
        'lower': ascii_lowercase,
        'mixed': ascii_letters
    }
    choices += cases[case]
    for _ in xrange(length):
        output += choice(choices)
    return output


class _Book:
    """
    Keeps the text of a book and the split sentences of a book
    globally available. This means you don't have to read in
    all of a book's text every time you need  a sentence or a set of words.
    The book will only be read once. The sentences of the book will only
    be split apart once.
    """
    # TODO: I really think Sherlock is a bad source for sentences.
    # There are just too many weird quotes and fragments. Too much dialog.
    def __init__(self):
        pass

    _path = join(dirname(
        __file__) + "/data/book_sherlock.txt")
    _text = _num_sentences = _sentences = None

    @classmethod
    def get_text(cls):
        if not cls._text:
            cls._text = open(cls._path).read()
        return cls._text

    @classmethod
    def get_sentences(cls):
        if not cls._sentences:
            text = cls.get_text()
            cls._sentences = _split_sentences(text)
            cls._num_sentences = len(cls._sentences)
        return cls._sentences

    @classmethod
    def gen_random_sentences(cls, no_more_than=1000000):
        sentences = cls.get_sentences()
        max_index = cls._num_sentences - 1
        for _ in xrange(no_more_than):
            i = randint(0, max_index)
            yield sentences[i]


def _split_sentences(text):
    # from pyteaser: https://github.com/xiaoxu193/PyTeaser
    # see `pyteaser.split_sentences()`
    fragments = split('(?<![A-Z])([.!?]"?)(?=\s+\"?[A-Z])', text)
    return map("".join, izip(*[iter(fragments[:-1])] * 2))


def sentence(num_words=20, chars=''):
    """
    Returns a sentence based on random words from The Adventures of
    Sherlock Holmes that is no more than `chars` characters in length
    or `num_words` words in length.
    """
    word_list = _Book.get_text().split()
    words = ' '.join(choice(word_list) for _ in
                     xrange(num_words))
    return words if not chars else words[:chars]


def sentence_actual(min_words=3, max_words=1000):
    """
    Returns a sentence from The Adventures of Sherlock Holmes
    that contains at least `min_words` and no more than `max_words`.
    """
    _rewhite = compile(r"\s+")
    _rewhitesub = partial(_rewhite.sub, "")
    for x in _Book.gen_random_sentences():
        words = _rewhite.split(x)
        words = filter(None, map(_rewhitesub, words))
        x = " ".join(words)
        if x.endswith(("Mr.", "Mrs.", "Dr.", "Ms.", "Prof.")):
            continue
        if min_words <= len(x.split()) <= max_words:
            return x
    raise Exception("Couldn't find a sentence between \
        {0} and {1} words long".format(min_words, max_words))


def trash(picka_function):
    """
     :Summary: This method takes a function you pass in, and joins\
     the output with _random punctuation.
     :Date: Tue Feb 22 15:31:12 EST 2011.
     :Usage: picka.trash(picka.name) >>> 'D#o}y>l~e^'
    """
    return ''.join([str(char) + choice(str(punctuation))
                    for char in picka_function()])
