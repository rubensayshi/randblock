from flask import Blueprint, abort, g
from flask import request, redirect, render_template, Response, url_for, current_app as app
from randblock.backend.grid import Grid, Block, GridException
from collections import namedtuple
import math
import random
import json
from copy import copy

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
            if not size.magic:
                space -= size.count * size.surface
        
        return space
    
    def add_size(self, *args, **kwargs):
        if self.locked:
            raise Exception('locked')
        
        size = Size(self, *args, **kwargs)
        self.sizes.append(size)
        
        return size
    
class Size(object):
    def __init__(self, sizes, size, count = None, percentage = None, magic = False):
        self.sizes       = sizes
        self.size        = size
        self.fixed_count = count
        self.percentage  = percentage
        self.magic       = magic
    
    @property
    def count(self):
        self.sizes.locked = True
        
        if self.fixed_count:
            return self.fixed_count
        
        if self.percentage:
            surface = self.sizes.surface * self.percentage
            return int(math.ceil(surface / self.surface))
            
        elif self.magic:
            return int(math.floor(self.sizes.free_space / self.surface))
        else:
            raise Exception('No way to determine count')
    
    @property
    def surface(self):
        return self.size * self.size

articles = None
def get_articles():
    global articles
    if  not articles:
        with open('./articles.json') as f:
            articles = json.loads(f.read())
    
    return articles

@main.route('/')
def index():
    articles = copy(get_articles())
    articles.reverse()
    
    try:
        s = Sizes(20)
        large  = s.add_size(5, count      = 4)
        medium = s.add_size(3, percentage = 0.3)
        small  = s.add_size(2, percentage = 0.2)
        filler = s.add_size(1, magic      = True)
        
        grid = Grid(20, 20, s = "!")
        
        if large.count == 4:
            grid.random(Block(articles.pop(), large.size, large.size), 2, 3)
            grid.random(Block(articles.pop(), large.size, large.size), 11, 4)
            grid.random(Block(articles.pop(), large.size, large.size), 2, 11)
            grid.random(Block(articles.pop(), large.size, large.size), 12, 12)
        
        for i in range(0, medium.count):
            grid.random(Block(articles.pop(), medium.size, medium.size))
        for i in range(0, small.count):
            grid.random(Block(articles.pop(), small.size, small.size))
        for i in range(0, filler.count):
            grid.random(Block(articles.pop(), filler.size, filler.size))
    
        print len(articles)
    
        return render_template("index.html", grid = grid)        
    except GridException, ge:
        return render_template("exception.html", ge = ge), 500

