import warnings
import functools

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