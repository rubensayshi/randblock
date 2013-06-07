import json
import copy
from flask import Blueprint, render_template
from randblock.backend.grid import Grid, Block, GridException
from randblock.backend.size_distribution import SizeManager

main = Blueprint('main', __name__)


##################################
############# ROUTES #############
##################################
@main.route('/')
def index():
    articles = copy.copy(get_articles())
    articles.reverse()
    
    try:
        sm = SizeManager(20)
        large  = sm.add_size(5, count      = 4)
        medium = sm.add_size(3, percentage = 0.3)
        small  = sm.add_size(2, percentage = 0.2)
        filler = sm.add_size(1, magic      = True)
        
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


##################################
############ HELPERS #############
##################################
articles = None
def get_articles():
    global articles
    if  not articles:
        with open('./articles.json') as f:
            articles = json.loads(f.read())
    
    return articles

