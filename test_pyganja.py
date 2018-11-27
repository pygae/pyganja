import unittest
from pyganja import *


class TestCEFDrawing(unittest.TestCase):
    def test_draw_lines(self):
        from clifford.tools.g3c import random_line
        draw_objects([random_line() for i in range(10)])

    def test_print_scene(self):
        from clifford.tools.g3c import random_line
        gs = GanjaScene()
        gs.add_objects([random_line() for i in range(2)])
        print(gs)


if __name__ == '__main__':
    unittest.main()
