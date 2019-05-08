
"""
This file contains utilities for drawing objects in conformal geometric algebra
It requires the clifford library to operate and thus can only be used when clifford
is already installed
"""

import numpy as np
from clifford.g3c import *
from clifford.tools.g3c import *
from . import *


def to_conf_points(point_data, w, h):
    """
    This takes a 2D array of point data (h,w,3) and converts it
    into a [w*h,32] conformal value array
    """
    gadata_buffer = np.zeros((w*h, 32))
    for i in range(h):
        for j in range(w):
            temp = np.zeros(32)
            temp[1:4] = point_data[i,j,:]
            gadata_buffer[i*w + j,:] = val_up(temp)
    return gadata_buffer


def file_as_scene(filename):
    """
    Draws the contents of the .ga file
    """
    gs = GanjaScene()
    gs.add_objects([mv for mv in layout.load_ga_file(filename)])
    return gs
