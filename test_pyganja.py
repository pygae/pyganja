import unittest
from pyganja import *


class TestCEFDrawing(unittest.TestCase):
    def test_draw_lines(self):
        from clifford.tools.g3c import random_line
        draw_objects([random_line().value for i in range(10)])


if __name__ == '__main__':
    unittest.main()
