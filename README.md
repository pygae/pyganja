# pyganja
Visualisation library for geometric algebra with cefpython and ganja.js

This is a module for visualing Geometric Algebra from scripts and also from jupyter notebooks, 
it relies on [ganja.js](https://github.com/enkimute/ganja.js) to render Geometric Algebra objects. 
If you are calling its api from a script it will render them in a cefpython window or if you are in a notebook it can simply render in the notebook itself.

# Use
This library is not specifically tied to the [clifford](https://github.com/pygae/clifford) library 
but is designed to work well with it. An example of the syntax that you would use combining these two libraries:

```
from clifford.tools.g3c import random_line
from pyganja import *

draw([random_line() for i in range(10)])
```

This would spawn a cefpython window displaying the random lines that you have drawn.

# Installation
```
git clone git@github.com:hugohadfield/pyganja.git
cd pyganja
python3 setup.py install
```

# TODO
This is still very much a work in progress, currently it only handles conformal GA
