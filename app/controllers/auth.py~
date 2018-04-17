''' user login, signup'''

from flask import Blueprint, render_template, abort, redirect
from jinja2 import TemplateNotFound

from app import DB, LOGIN

from app.models.temp import Temp
from app.models.user import User

from app.controllers.forms.login import LoginForm

AUTH = Blueprint('auth', __name__,
                 template_folder='templates')

@LOGIN.user_loader
def load_user(id):
    return User.query.get(int(id))


@AUTH.route('/login', methods=['GET', 'POST'])
def login():
    '''login'''
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/baa')
    return render_template("login.html", form=form, title='Log in')
