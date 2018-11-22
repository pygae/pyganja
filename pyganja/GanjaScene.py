
import json


class GanjaScene:

    def __init__(self):
        self.internal_list = []

    def add_object(self, mv_array, color=int('AA000000', 16), label=None):
        if label is not None:
            try:
                assert isinstance(label, str)
                self.internal_list.append(label)
            except:
                raise ValueError('Labels must be strings')
        self.internal_list.append(color)
        self.internal_list.append([i for i in mv_array])

    def add_objects(self, mv_list, color=int('AA000000', 16), label=None):
        if label is not None:
            try:
                assert isinstance(label, str)
                self.internal_list.append(label)
            except:
                raise ValueError('Labels must be strings')
        self.internal_list.append(color)
        for mv_array in mv_list:
            self.internal_list.append([i for i in mv_array])

    def __repr__(self):
        return json.dumps(self.internal_list)

    def save_to_file(self, filename):
        with open(filename, 'w') as fobj:
            print(self, file=fobj)

