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
Produces:
![Random lines](./random_lines.png?raw=true)


Mulitple grades of object can be drawn in the same scene with different colors and transparencies
```
from clifford.g3c import *
from clifford.tools.g3c import *
from pyganja import *

P1 = up(random_euc_mv()*0.1)
P2 = up(random_euc_mv()*0.1)
P3 = up(random_euc_mv()*0.1)
P4 = up(random_euc_mv()*0.1)

# The sphere is the outer product of all 4
S = (P1^P2^P3^P4).normal()

# A line is the outer product of 2 with ninf
L = P1^P2^einf

# The inversion of a line in a sphere is a circle
C = S*L*S

# The tangent to the circle at the intersection point is the reflected line
Ldash = (P1|C)^einf

# The tangent plane to the sphere at the intersection point can be easily found
Ppi = (P1|S)^einf

sc = GanjaScene()
sc.add_objects([P1,P2,P3,P4], color=Color.BLACK)
sc.add_objects([L], color=Color.BLUE)
sc.add_objects([Ldash], color=Color.RED)
sc.add_objects([C], color=Color.RED)
sc.add_objects([S*einf*S], color=Color.BLACK)
sc.add_objects([S])
sc.add_objects([Ppi], color=rgb2hex((0,100,0))+int('70000000',16))
draw(sc,scale=0.5)
```
Produces:
![Sphere reflection](./line_sphere_reflect.png?raw=true)

# Installation
```
git clone git@github.com:hugohadfield/pyganja.git
cd pyganja
python3 setup.py install
```

# TODO
This is still very much a work in progress, currently it only handles PGA and CGA
