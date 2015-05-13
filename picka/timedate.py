import random
import calendar
import time

def month():
    return random.choice(calendar.month_name[1:])


def month_and_day():
    """Selects and month and day for you.
    There is logic to handle the days in the month correctly.
    """

    month_choice = month()
    if month_choice in [
        'January', 'March', 'May', 'July', 'August',
        'October', 'December'
    ]:
        return '%s %s' % (month_choice, random.randrange(1, 32))
    if month_choice in 'February':
        return '%s %s' % (month_choice, random.randrange(1, 29))
    else:
        return '%s %s' % (month_choice, random.randrange(1, 31))


def month_and_day_and_year(start=1900, end=2010):
    """
    Selects a monday, day and year for you.
    Logic built in to handle day in month.
    To change month do (a, b). b has +1 so the
    last year in your range can be selected. Default is 1900, 2010.
    """

    return '%s %s' % (month_and_day(), random.randrange(start, end + 1))


def timestamp(style=False):
    """
    This is a convenience function for creating timestamps.
    Default when empty, is "12:28:59PM 07/20/10" or "%H:%M:%S%p %D".
    To change this, pass in your format as an arg.
    """

    if not style:
        return time.strftime('%H:%M:%S%p %x', time.localtime())
    else:
        return time.strftime(style, time.localtime())


def timezone_offset():
    """
    This function will select the value of a timezone offsets,
    such as GMT, GMT+4, etc.
    """

    return random.choice(
        [
            ['GMT+' + str(random.randint(1, 12))],
            ['GMT'],
            ['GMT' + str(random.randint(-12, -1))]
        ]
    )[0]


def timezone_offset_country():
    """This function will select the country part of a timezone."""

    return random.choice(
        [
            'Eniwetoa',
            'Hawaii',
            'Alaska',
            'Pacific',
            'Mountain',
            'Central',
            'Eastern',
            'Atlantic',
            'Canada',
            'Brazilia',
            'Buenos Aries',
            'Mid-Atlantic',
            'Cape Verdes',
            'Greenwich Mean Time',
            'Dublin',
            'Berlin',
            'Rome',
            'Israel',
            'Cairo',
            'Moscow',
            'Kuwait',
            'Abu Dhabi',
            'Muscat',
            'Islamabad',
            'Karachi',
            'Almaty',
            'Dhaka',
            'Bangkok, Jakarta',
            'Hong Kong',
            'Beijing',
            'Tokyo',
            'Osaka',
            'Sydney',
            'Melbourne',
            'Guam',
            'Magadan',
            'Soloman Islands',
            'Fiji',
            'Wellington',
            'Auckland',
        ]
    )

