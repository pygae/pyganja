
from enum import Enum

def rgb2hex(x):
    if len(x) == 3:
        return int('%02x%02x%02x' %(int(x[0]),int(x[1]),int(x[2])),16)
    elif len(x) == 4:
        return int('%02x%02x%02x%02x' %(int(x[0]),int(x[1]),int(x[2]),int(x[3])),16)
    else:
        raise ValueError('X must be of length 3 or 4, ie. an rgb or argb array')

class Color(Enum):
    BLUE = int('000000FF', 16)
    RED = int('00FF0000', 16)
    GREEN = int('0000FF00', 16)
    YELLOW = int('00FFFF00', 16)
    MAGENTA = int('00FF00FF', 16)
    CYAN = int('0000FFFF', 16)
    BLACK = int('00000000', 16)
