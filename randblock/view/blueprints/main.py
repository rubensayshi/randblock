from flask import Blueprint, abort
from flask import request, redirect, render_template, Response, url_for, current_app as app
from randblock.backend.grid import Grid, Block, GridException

main = Blueprint('main', __name__)

##################################
############# ROUTES #############
##################################

@main.route('/')
def index():
    try:
        grid = Grid(10, 10, s = "!")
        
        grid.random(Block('red', 7, 7))
        grid.random(Block('blue', 3, 3))
        grid.random(Block('pink', 1, 1))
        grid.random(Block('yellow', 1, 1))
        grid.random(Block('green', 3, 3))
        grid.random(Block('black', 1, 1))
        grid.random(Block('white', 1, 1))
        grid.random(Block('black', 1, 1))
        grid.random(Block('white', 1, 1))
    
        return render_template("index.html", grid = grid)        
    except GridException, ge:
        return render_template("exception.html", ge = ge), 500

