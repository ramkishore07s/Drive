'''not decided
'''

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

MAIN = Blueprint('main', __name__,
                 template_folder='templates')

@MAIN.route('/baa')
def show():
    '''show'''
    return render_template("index.html")
