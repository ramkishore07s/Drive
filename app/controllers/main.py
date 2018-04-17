'''not decided
'''

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from app import DB, session

from app.models.temp import Temp
from app.models.user import User

from app.controllers.forms.login import LoginForm

MAIN = Blueprint('main', __name__,
                 template_folder='templates')

@MAIN.route('/baa')
def show():
    '''show'''
    return "You have logged in"
