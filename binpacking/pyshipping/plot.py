# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import numpy as np
from itertools import product, combinations

class Cube:
    x = y = z = 0
    w = l = h = 0
    
    color = 'b'
    
    ax = None
    parent = None
    
    def __init__(self):
        self.items = []
        for a in ('heigth', 'width', 'length'):
            if hasattr(self, a):
                value = getattr(self, a)
                setattr(self, a[0], value)
    
    def add(self, item):
        self.items.append(item)
        
        item.parent = self
        
    def get_abs_pos(self, coord):
        pos = getattr(self, coord)
        if self.parent:
            pos += self.parent.get_abs_pos(coord)
        return pos
    
#     @property
    def coords(self):      
        x = self.get_abs_pos('x')
        y = self.get_abs_pos('y')
        z = self.get_abs_pos('z')
        
        return x, y, z
        
#         w, l, h = self.w, self.l, self.h
#         
#         x, y, z, w, l, h = self.scale(x, y, z, w, l, h)
#         
#         return [
#             [x, x + w, x + w, x,     x, x,     x,     x,      x,     x + w, x + w, x + w, x + w, x + w, x + w, x,     x],
#             [y, y,     y,     y,     y, y + l, y + l, y,      y + l, y + l, y,     y,     y + l, y + l, y + l, y + l, y],
#             [z, z,     z + h, z + h, z, z,     z + h, z + h , z + h, z + h, z + h, z,     z,     z + h, z,     z,     z]]
    
    def scale(self, x, y, z, w, l, h):
        return x, y, z, w, l, h
    
    def calc(self):
        self.x, self.y, self.z = self.coords()
        for item in self.items:
            item.calc()
            1 / 0
    
    def draw(self, ax=None): pass
#         if ax is None:
#             fig = plt.figure()
#             ax = fig.gca(projection='3d')
#             ax.set_aspect("equal")
#         
#         for item in self.items:
#             item.draw(ax)
#         
#         ax.plot(*self.coords, color=self.color)
    
    def save(self, filename): pass
#         plt.savefig(filename)
        
    def __repr__(self):
        return "%dx%dx%d (%s, %s, %s)" % (self.w, self.l, self.h, self.x, self.y, self.z)

class Strip(Cube):
    color = 'r'
    def add(self, package):
        Cube.add(self, package)
        
        package.z = self.h
        
        self.h += package.heigth
        self.w = max(self.w, package.width)
        self.l = max(self.l, package.length)

class Layer(Cube):
    color = 'g'
    def add(self, strip):
        Cube.add(self, strip)
        
        strip.x = self.w
        
        self.w += strip.w
        self.h = max(self.h, strip.h)
        self.l = max(self.l, strip.l)

class Bin(Cube):
    color = '000000'
    def add(self, layer):
        Cube.add(self, layer)
        
        layer.y = self.l
        
        self.l += layer.l
        self.w = max(self.w, layer.w)
        self.h = max(self.h, layer.h)
        