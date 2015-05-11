import warnings
import functools
import datetime


warnings.simplefilter('always', DeprecationWarning)


def deprecated(replacement=None):
    def outer(fun):
        msg = "picka.%s is deprecated" % fun.__name__
        if replacement is not None:
            msg += "; use %s instead" % replacement
        if fun.__doc__ is None:
            fun.__doc__ = msg

        @functools.wraps(fun)
        def inner(*args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            return fun(*args, **kwargs)

        return inner

    return outer


def _ssn_prefixes(state):
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


def _readable_date(theDateAndTime, fromDate, precise=False):
    """ provides a human readable format for a time delta
        @param theDateAndTime this is time equal or older than now or the date in 'fromDate'
        @param precise        when true then milliseconds and microseconds are included
        @param fromDate       when None the 'now' is used otherwise a concrete date is expected
        @return the time delta as text

        @note I don't calculate months and years because those varies (28,29,30 or 31 days a month
              and 365 or 366 days the year depending on leap years). In addition please refer
              to the documentation for timedelta limitations.
    """
    if not fromDate:
        fromDate = datetime.now()

    if theDateAndTime > fromDate:
        return None
    elif theDateAndTime == fromDate:
        return "now"

    delta = fromDate - theDateAndTime

    # the timedelta structure does not have all units; bigger units are converted
    # into given smaller ones (hours -> seconds, minutes -> seconds, weeks > days, ...)
    # but we need all units:
    deltaMinutes = delta.seconds // 60
    deltaHours = delta.seconds // 3600
    deltaMinutes -= deltaHours * 60
    deltaWeeks = delta.days // 7
    deltaSeconds = delta.seconds - deltaMinutes * 60 - deltaHours * 3600
    deltaDays = delta.days - deltaWeeks * 7
    deltaMilliSeconds = delta.microseconds // 1000
    deltaMicroSeconds = delta.microseconds - deltaMilliSeconds * 1000

    valuesAndNames = [(deltaWeeks, "week"  ), (deltaDays, "day"   ),
                      (deltaHours, "hour"  ), (deltaMinutes, "minute"),
                      (deltaSeconds, "second")]
    if precise:
        valuesAndNames.append((deltaMilliSeconds, "millisecond"))
        valuesAndNames.append((deltaMicroSeconds, "microsecond"))

    text = ""
    for value, name in valuesAndNames:
        if value > 0:
            text += len(text) and ", " or ""
            text += "%d %s" % (value, name)
            text += (value > 1) and "s" or ""

    # replacing last occurrence of a comma by an 'and'
    if text.find(",") > 0:
        text = " and ".join(text.rsplit(", ", 1))

    return text