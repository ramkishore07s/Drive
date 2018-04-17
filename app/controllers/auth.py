''' user login, signup'''
import os

from flask import Blueprint, render_template, abort, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user

from jinja2 import TemplateNotFound

from app import DB, LOGIN, APP

from app.models.user import User

from app.controllers.forms.auth import LoginForm, SignupForm

AUTH = Blueprint('auth', __name__,
                 template_folder='templates')

@LOGIN.user_loader
def load_user(id):
    return User.query.get(int(id))


@AUTH.route('/login', methods=['GET', 'POST'])
def login():
    '''login'''
    if current_user.is_authenticated:
        return redirect('/mydrive')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
        else:
            login_user(user, remember=form.remember_me.data)
        return redirect('login')
    return render_template("login.html", form=form, title='Log in')

@AUTH.route('/signup', methods=['GET', 'POST'])
def signup():
    '''signup'''
    if current_user.is_authenticated:
        return redirect('/mydrive')
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            if form.password.data == form.confirm_password.data:

                # -------------- create user ---------------
                
                new_user = User(form.username.data, form.email.data, form.password.data)
                DB.session.add(new_user)
                DB.session.commit()

                # ------------- create drive --------------

                user_space = os.makedirs(APP.config['UPLOAD_FOLDER'] + "/" + str(new_user.id))
                   
                return redirect(url_for('auth.login'))
            flash("passwords don't match")
        else:
            flash("email already taken")
    return render_template("signup.html", form=form, title="Sign Up")
            
@AUTH.route('/logout')
def logout():
    '''logout'''
    logout_user()
    return redirect(url_for("auth.login"))
