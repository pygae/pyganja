import numbers
from enum import IntEnum
import operator

def rgb2hex(x):
    if len(x) in (3, 4):
        val = 0
        for xi in x:
            val = (val << 8) | _entry_as_uint8(xi)
        return val
    else:
        raise ValueError('X must be of length 3 or 4, ie. an rgb or argb array')


def _entry_as_uint8(v):
    if isinstance(v, numbers.Integral):
        if v > 255:
            return 255
        elif v < 0:
            return 0
        else:
            return operator.index(v)
    else:
        raise TypeError("Can't convert {!r} to a color component".format(v))


def as_hex(x):
    """ Convert any vague color description to a hex color """
    try:
        return operator.index(x)
    except TypeError:
        return rgb2hex(x)


class Color(IntEnum):
    BLUE = 0x000000FF
    RED = 0x00FF0000
    GREEN = 0x0000FF00
    YELLOW = 0x00FFFF00
    MAGENTA = 0x00FF00FF
    CYAN = 0x0000FFFF
    BLACK = 0x00000000
    DEFAULT = 0xAA000000
