import unittest
from pyganja import *


class TestCEFDrawing(unittest.TestCase):
    def test_draw_lines(self):
        from clifford.tools.g3c import random_line
        draw([random_line() for i in range(10)], static=True, color=Color.RED)

    def test_print_scene(self):
        from clifford.tools.g3c import random_line
        gs = GanjaScene()
        gs.add_objects([random_line() for i in range(2)])
        print(gs)


class TestCGADrawing(unittest.TestCase):
    def test_pyganja_facet(self):
        from clifford.tools.g3c import random_conformal_point
        from pyganja import GanjaScene
        gs = GanjaScene()
        point_list = [random_conformal_point() for i in range(3)]
        #gs.add_objects(point_list)
        gs.add_facet(point_list)
        point_list = [random_conformal_point() for i in range(3)]
        #gs.add_objects(point_list)
        #gs.add_facet(point_list,color=int('AAFF0000',16))
        facet_list = [[random_conformal_point() for i in range(3)] for i in range(10)]
        #gs.add_facets(facet_list,color=int('AA0000FF',16))
        draw(gs, scale=0.05, browser_window=True)
        print(gs)


class TestG3Drawing(unittest.TestCase):
    def test_draw_points(self):
        from clifford.tools.g3 import random_euc_mv
        from clifford.g3 import layout
        gs = GanjaScene()
        gs.add_objects([random_euc_mv().value[0:8] for i in range(10)], static=False)
        with open('test_file.html', 'w') as test_file:
            test_file.write(generate_full_html(str(gs), sig=layout.sig, grid=True, scale=1.0, gl=True))
        render_cef_script(str(gs), sig=layout.sig, grid=True, scale=1.0, gl=False)


class TestPGA3DDrawing(unittest.TestCase):

    def setUp(self):
        from clifford.pga import layout, blades
        import numpy as np
        self.layout = layout
        self.blades = blades
        self.np = np

    def random_point(self):
        return sum(c * b for c, b in
                   zip(self.np.random.randn(3), [self.blades["e023"], self.blades["e013"], self.blades["e012"]])) + \
               self.blades["e123"]

    def test_draw_points(self):
        gs = GanjaScene()
        gs.add_objects([self.random_point() for i in range(10)], static=False)
        with open('test_file.html', 'w') as test_file:
            test_file.write(generate_full_html(str(gs), sig=self.layout.sig, grid=True, scale=1.0, gl=True))
        draw(gs, sig=self.layout.sig, grid=True, scale=1.0, gl=True)

    def test_draw_lines(self):

        def random_line():
            return (self.random_point().dual()^self.random_point().dual()).dual()

        gs = GanjaScene()
        gs.add_objects([random_line() for i in range(10)], static=False)
        with open('test_file.html', 'w') as test_file:
            test_file.write(generate_full_html(str(gs), sig=self.layout.sig, grid=True, scale=1.0, gl=True))
        draw(gs, sig=self.layout.sig, grid=True, scale=1.0, gl=True)

    def test_draw_planes(self):
        gs = GanjaScene()
        gs.add_objects([self.random_point().dual() for i in range(10)], static=False)
        with open('test_file.html', 'w') as test_file:
            test_file.write(generate_full_html(str(gs), sig=self.layout.sig, grid=True, scale=1.0, gl=True))
        draw(gs, sig=self.layout.sig, grid=True, scale=1.0, gl=True)


class TestGanjaSceneOps(unittest.TestCase):
    def test_scene_addition(self):
        from clifford.tools.g3c import random_line, random_circle
        a = GanjaScene()
        a.add_objects([random_line() for i in range(10)], color=Color.RED)
        b = GanjaScene()
        b.add_objects([random_circle() for i in range(10)], color=Color.BLUE)
        draw(a + b, scale=0.01)


class TestPGADrawing(unittest.TestCase):
    def test_draw_lines(self):
        from clifford.pga import layout, blades
        p = 0.5*blades['e1'] + 0.5*blades['e2'] + 1.0*blades['e0']
        print(p)
        draw([p], sig=layout.sig)


if __name__ == '__main__':
    unittest.main()
