from flask import Blueprint, abort
from flask import request, redirect, render_template, Response, url_for, current_app as app
from randblock.backend.grid import Grid, Block, GridException
from collections import namedtuple
import math

main = Blueprint('main', __name__)

##################################
############# ROUTES #############
##################################

class Sizes(object):
    def __init__(self, size):
        self.locked = False
        self.size = size
        self.sizes = []
    
    @property
    def surface(self):
        return self.size * self.size
    
    @property
    def free_space(self):
        space = self.surface
        for size in self.sizes:
            if size.percentage:
                space -= size.count * size.surface
        
        return space
    
    def add_size(self, *args, **kwargs):
        if self.locked:
            raise Exception('locked')
        
        size = Size(self, *args, **kwargs)
        self.sizes.append(size)
        
        return size
    
class Size(object):
    def __init__(self, sizes, size, percentage = None):
        self.sizes      = sizes
        self.size       = size
        self.percentage = percentage
    
    @property
    def count(self):
        self.sizes.locked = True
        
        if self.percentage:
            surface = self.sizes.surface * self.percentage
            count   = int(math.ceil(surface / self.surface))
            
            return count
        else:
            count = int(math.floor(self.sizes.free_space / self.surface))
            
            return count
    
    @property
    def surface(self):
        return self.size * self.size

@main.route('/')
def index():
    try:
        s = Sizes(20)
        large  = s.add_size(8, 0.4)
        medium = s.add_size(4, 0.3)
        small  = s.add_size(1, None)
        
        grid = Grid(20, 20, s = "!")
        
        for i in range(0, large.count):
            grid.random(Block('red', large.size, large.size))
        for i in range(0, medium.count):
            grid.random(Block('blue', medium.size, medium.size))
        for i in range(0, small.count):
            print "BLOCK"
            grid.random(Block('green', small.size, small.size), 1, 0)
    
        return render_template("index.html", grid = grid)        
    except GridException, ge:
        return render_template("exception.html", ge = ge), 500

