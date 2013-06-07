from flask import Blueprint, abort
from flask import request, redirect, render_template, Response, url_for, current_app as app

main = Blueprint('main', __name__)

##################################
############# ROUTES #############
##################################

@main.route('/')
def index():
    return render_template("index.html")

