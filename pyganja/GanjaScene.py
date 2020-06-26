
import json
from . import color as _color


def _as_list(mv_array):
    # clifford.multivector
    if hasattr(mv_array, 'value'):
        mv_array = mv_array.value

    # numpy array, which contains non-json.dumps-able scalars
    try:
        import numpy as np
    except ImportError:
        pass
    else:
        if isinstance(mv_array, np.ndarray):
            mv_array = mv_array.tolist()

    # any other sequence
    if not isinstance(mv_array, list):
        mv_array = list(mv_array)

    return mv_array


class GanjaScene:

    def __init__(self):
        self.internal_list = []
        self.mv_length = None

    def __add__(self, other):
        if isinstance(other, GanjaScene):
            gs = GanjaScene()
            gs.internal_list = self.internal_list + other.internal_list
            if self.mv_length is not None:
                gs.mv_length = self.mv_length
            else:
                gs.mv_length = other.mv_length
            return gs
        else:
            raise ValueError('The objects being added are not both GanjaScenes...')

    def add_object(self, mv_array, color=0xAA000000, label=None, static=False):
        mv_list = _as_list(mv_array)
        self.mv_length = len(mv_list)
        self.internal_list.append(_color.as_hex(color))
        if static:
            self.internal_list.append({'data': [mv_list]})
        else:
            self.internal_list.append(mv_list)
        if label is not None:
            try:
                assert isinstance(label, str)
                self.internal_list.append(label)
            except:
                raise ValueError('Labels must be strings')

    def add_facet(self, mv_list, color=0xAA000000, label=None, static=False):
        self.internal_list.append(_color.as_hex(color))
        facet_list = []
        for mv_array in mv_list:
            mv_list = _as_list(mv_array)
            facet_list.append(mv_list)
            self.mv_length = len(mv_list)
        if static:
            self.internal_list.append({'data': [facet_list]})
        else:
            self.internal_list.append(facet_list)
        if label is not None:
            try:
                assert isinstance(label, str)
                self.internal_list.append(label)
            except:
                raise ValueError('Labels must be strings')

    def add_facets(self, mv_vertex_list, color=0xAA000000, label=None, static=False):
        for mv_array in mv_vertex_list:
            self.add_facet(mv_array, color=color, label=label, static=static)
        if label is not None:
            try:
                assert isinstance(label, str)
                self.internal_list.append(label)
            except:
                raise ValueError('Labels must be strings')

    def add_objects(self, mv_object_list, color=0xAA000000, label=None, static=False):
        self.internal_list.append(_color.as_hex(color))
        static_list = []
        for mv_array in mv_object_list:
            mv_list = _as_list(mv_array)
            self.mv_length = len(mv_list)
            if static:
                static_list.append(mv_list)
            else:
                self.internal_list.append(mv_list)
        if static:
            self.internal_list.append({'data': static_list})
        if label is not None:
            try:
                assert isinstance(label, str)
                self.internal_list.append(label)
            except:
                raise ValueError('Labels must be strings')

    def __repr__(self):
        if self.mv_length is None:
            new_str = '[]'
        else:
            new_str = str.replace(json.dumps(self.internal_list), '''"data": ''', 'data:')
            new_str = str.replace(new_str, ']}', """].map(x=>x.length=="""+str(self.mv_length)+"""?new Element(x):x)}""")
            new_str = str.replace(new_str, ']]',
                                  """]].map(x=>x.length==""" + str(self.mv_length) + """?new Element(x):x)""")
        return new_str

    def save_to_file(self, filename):
        with open(filename, 'w') as fobj:
            print(self, file=fobj)

