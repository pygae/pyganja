import unittest
from pyganja import *


class TestCEFDrawing(unittest.TestCase):
    def test_draw_lines(self):
        from clifford.tools.g3c import random_line
        draw([random_line() for i in range(10)], static=True)

    def test_print_scene(self):
        from clifford.tools.g3c import random_line
        gs = GanjaScene()
        gs.add_objects([random_line() for i in range(2)])
        print(gs)


class TestG3Drawing(unittest.TestCase):
    def test_draw_points(self):
        from clifford.tools.g3 import random_euc_mv
        from clifford.g3 import layout
        gs = GanjaScene()
        gs.add_objects([random_euc_mv().value[0:8] for i in range(10)], static=False)
        with open('test_file.html','w') as test_file:
            print(generate_full_html(str(gs), sig=layout.sig, grid=True, scale=1.0, gl=False), file=test_file)
        render_cef_script(str(gs), sig=layout.sig, grid=True, scale=1.0, gl=False)


if __name__ == '__main__':
    unittest.main()
