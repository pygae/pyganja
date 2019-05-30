
import json
import enum


class GanjaScene:

    def __init__(self):
        self.internal_list = []
        self.mv_length = 32

    def __add__(self, other):
        if isinstance(other, GanjaScene):
            gs = GanjaScene()
            gs.internal_list = self.internal_list + other.internal_list
            return gs
        else:
            raise ValueError('The objects being added are not both GanjaScenes...')

    def add_object(self, mv_array, color=int('AA000000', 16), label=None, static=False):
        self.mv_length = len(mv_array)
        if isinstance(color, enum.Enum):
            self.internal_list.append(color.value)
        else:
            self.internal_list.append(color)
        if static:
            self.internal_list.append({'data': [[i for i in mv_array]]})
        else:
            self.internal_list.append([i for i in mv_array])
        if label is not None:
            try:
                assert isinstance(label, str)
                self.internal_list.append(label)
            except:
                raise ValueError('Labels must be strings')

    def add_facet(self, mv_list, color=int('AA000000', 16), label=None, static=False):
        if isinstance(color, enum.Enum):
            self.internal_list.append(color.value)
        else:
            self.internal_list.append(color)
        facet_list = []
        for mv_array in mv_list:
            facet_list.append([i for i in mv_array])
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

    def add_facets(self, mv_list, color=int('AA000000', 16), label=None, static=False):
        for mv_array in mv_list:
            self.add_facet(mv_array,color=color, label=label, static=static)
        if label is not None:
            try:
                assert isinstance(label, str)
                self.internal_list.append(label)
            except:
                raise ValueError('Labels must be strings')

    def add_objects(self, mv_list, color=int('AA000000', 16), label=None, static=False):
        if isinstance(color, enum.Enum):
            self.internal_list.append(color.value)
        else:
            self.internal_list.append(color)
        static_list = []
        self.mv_length = len(mv_list[0])
        for mv_array in mv_list:
            if static:
                static_list.append([i for i in mv_array])
            else:
                self.internal_list.append([i for i in mv_array])
        if static:
            self.internal_list.append({'data': static_list})
        if label is not None:
            try:
                assert isinstance(label, str)
                self.internal_list.append(label)
            except:
                raise ValueError('Labels must be strings')

    def __repr__(self):
        new_str = str.replace(json.dumps(self.internal_list), '''"data": ''', 'data:')
        new_str = str.replace(new_str, ']}', """].map(x=>x.length=="""+str(self.mv_length)+"""?new Element(x):x)}""")
        new_str = str.replace(new_str, ']]',
                              """]].map(x=>x.length==""" + str(self.mv_length) + """?new Element(x):x)""")
        return new_str

    def save_to_file(self, filename):
        with open(filename, 'w') as fobj:
            print(self, file=fobj)

