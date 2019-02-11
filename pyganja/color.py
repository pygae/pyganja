
from enum import Enum

class Color(Enum):
    BLUE = int('000000FF', 16)
    RED = int('00FF0000', 16)
    GREEN = int('0000FF00', 16)
    YELLOW = int('00FFFF00', 16)
    MAGENTA = int('00FF00FF', 16)
    CYAN = int('0000FFFF', 16)
    BLACK = int('00000000', 16)
