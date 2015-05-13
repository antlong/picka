#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Picka is a data generation and randomization module which aims to increase
coverage by increasing the amount of tests you _dont_ have to write
by hand.
By: Anthony Long
"""

from functools import partial
import string
import random as _random
import random
import re
import socket
import struct
from ConfigParser import ConfigParser

import picka_utils as _utils
from english import name as _name


__docformat__ = 'restructuredtext en'
_query = _utils.query
name = _name



class _Settings(ConfigParser):
    defaults = {
        'output': 'full',
    }

    def get(self, section, key):
        try:
            return ConfigParser.get(self, section, key)
        except ConfigParser.NoSectionError:
            if section in self.defaults:
                self.add_section(section)
                self.set(section, key, self.defaults[section])
                return self.defaults[section]
            else:
                raise
        except ConfigParser.NoOptionError:
            if section in self.defaults:
                self.set(section, key, self.defaults[section])
                return self.defaults[section]
            else:
                raise


def trash(picka_function):
    """
     :Summary: This method takes a function you pass in, and joins\
     the output with random punctuation.
     :Date: Tue Feb 22 15:31:12 EST 2011.
     :Usage: picka.trash(picka.name) >>> 'D#o}y>l~e^'
    """
    return ''.join([str(char) + _random.choice(str(string.punctuation))
                    for char in picka_function()])


def number(length=1):
    """This function will produce a random number with as many
    characters as you wish.
    """
    return ''.join(str(_random.randrange(0, 10)) for _ in xrange(length))

def sentence(num_words=20, chars=''):
    """
    Returns a sentence based on random words from The Adventures of
    Sherlock Holmes that is no more than `chars` characters in length
    or `num_words` words in length.
    """
    word_list = _Book.get_text().split()
    words = ' '.join(_random.choice(word_list) for _ in
                     xrange(num_words))
    return words if not chars else words[:chars]


def sentence_actual(min_words=3, max_words=1000):
    """
    Returns a sentence from The Adventures of Sherlock Holmes
    that contains at least `min_words` and no more than `max_words`.
    """
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


def foreign_characters(i):
    foreign_chars = (
        u'ƒŠŒŽšœžŸÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕ\
        ÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'
    )
    return ''.join(_random.choice(foreign_chars) for _ in xrange(i))


def special_characters(i):
    """
    This function will pick x amount of special chars from the list below.
    ie - picka.special_characters() = '@%^$'.
    """

    return ''.join(_random.choice(string.punctuation) for _ in xrange(i))


def rbg():
    return [_random.randint(0, 256) for _ in xrange(3)]


def rbga(a=0):
    x = rbg()
    x.append(a) if isinstance(a, (
        int, long)) else x.append(_random.randint(0, 256))
    return x


# noinspection PyUnresolvedReferences
def image(filepath, length=100, width=100, a=0):
    """Generate a random colored image, with random text on it.
    Returns filepath for ease of use.

        :param: filepath: path to save image to.
        :type filepath: str
        :param length: length of the image
        :type length: int
        :param width: width of the image
        :type width: int
    """
    try:
        import Image
        import ImageDraw
    except ImportError as e:
        print e, "Please install PIL to use this functionality."
        return
    im = Image.new('RGBA', tuple((length, width)), tuple((rbga(a))))
    draw = ImageDraw.Draw(im)
    text = sentence_actual(1)
    draw.text((0, 0), text, fill=rbg())
    im.save(filepath)
    return filepath


def hex_color():
    def _chkarg(a):
        if isinstance(a, int):
            if a < 0:
                a = 0
            elif a > 255:
                a = 255
        elif isinstance(a, float):
            if a < 0.0:
                a = 0
            elif a > 1.0:
                a = 255
            else:
                a = int(round(a * 255))
        return a

    r, b, g = rbg()
    r = _chkarg(r)
    g = _chkarg(g)
    b = _chkarg(b)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def barcode(specification="EAN-8"):
    """Based on the standard barcode specifications. Valid options are:
    EAN-8 - 8 numerical digits.
    EAN-13 - 13 numerical digits.
    UPC-A - Used on products at the point of sale

    Unsupported, but in-progress:
    UPC-B - Developed for the US National Drug Code; used to identify drugs
    UPC-E - Used on smaller products where 12 digits don’t fit
    UPC-5 - Used as a supplemental code to indicate the price of retail books
    """

    def _gen(i):
        upc_str = str(i)
        odd_sum = 0
        even_sum = 0
        for i, char in enumerate(upc_str):
            j = i + 1
            if j % 2 == 0:
                even_sum += int(char)
            else:
                odd_sum += int(char)
        total_sum = (odd_sum * 3) + even_sum
        mod = total_sum % 10
        check_digit = 10 - mod
        if check_digit == 10:
            check_digit = 0
        return upc_str + str(check_digit)

    if specification == "EAN-8":
        return _gen(number(7))

    if specification == "EAN-13":
        return _gen(number(12))

    if specification == "UPC-A":
        return _gen(number(11))


def mime_type():
    """Returns tuple, left is suffix, right is media type/subtype.
    """
    cursor.execute('SELECT extension,name FROM mimes WHERE id =?', [
        _random.randint(1, _get_max("mimes"))])
    return cursor.fetchone()


def ipv4():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))


settings = _Settings()