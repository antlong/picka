#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Picka is a data generation and randomization module which aims to increase
coverage by increasing the amount of tests you _dont_ have to write
by hand.
By: Anthony Long
"""
import string
from random import choice, randint
import socket as _socket
import struct as _struct

import picka_utils as _utils
from numbers import number
import db as _db

_query = _db.query()
_row_counts = _utils.row_counts


def trash(picka_function):
    """
     :Summary: This method takes a function you pass in, and joins\
     the output with _random punctuation.
     :Date: Tue Feb 22 15:31:12 EST 2011.
     :Usage: picka.trash(picka.name) >>> 'D#o}y>l~e^'
    """
    return ''.join([str(char) + choice(str(string.punctuation))
                    for char in picka_function()])


def foreign_characters(i):
    foreign_chars = (
        u'ƒŠŒŽšœžŸÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕ\
        ÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'
    )
    return ''.join(choice(foreign_chars) for _ in xrange(i))


def special_characters(i):
    """
    This function will pick x amount of special chars from the list below.
    ie - picka.special_characters() = '@%^$'.
    """

    return ''.join(choice(string.punctuation) for _ in xrange(i))


def rbg():
    return [randint(0, 256) for _ in xrange(3)]


def rbga(a=0):
    x = rbg()
    x.append(a) if isinstance(a, (
        int, long)) else x.append(randint(0, 256))
    return x


# noinspection PyUnresolvedReferences
def image(filepath, length=100, width=100, a=0):
    """Generate a _random colored image, with _random text on it.
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
    return _query("extension,name", "mimes")


def ipv4():
    return _socket.inet_ntoa(_struct.pack('>I', randint(1, 0xffffffff)))
