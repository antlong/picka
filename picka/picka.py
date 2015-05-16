#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
from random import choice, randint
from socket import inet_ntoa
from struct import pack

from numerics import number
from picka_utils import engine_connection

engine = engine_connection

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
    return query_multiple("extension,name", "mimes")

class IP(object):
    @staticmethod
    def ipv4():
        return inet_ntoa(pack('>I', randint(1, 0xffffffff)))

