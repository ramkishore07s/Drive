''' Init module
'''

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_sqlalchemy import SQLAlchemy

from app.controllers.main import MAIN

from app.models.shared import db
from app.models.temp import Temp

APP = Flask(__name__)
APP.register_blueprint(MAIN)


APP.config.from_object(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
APP.config.update(dict(
    DATABASE=os.path.join(APP.root_path, 'app.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
APP.config.from_envvar('FLASKR_SETTINGS', silent=True)

with APP.app_context():
    db.init_app(APP)
    db.create_all()

    a = Temp("a", "b", "c", "d")
    db.session.add(a)
    db.session.commit()

@APP.route('/')
def hello_world():
    '''hello world'''
    return render_template("app.html")

@APP.route('/aba')
def checking():
    '''checking'''
    return 'bleh bleh bleh'


if __name__ == '__main__':
    APP.run(debug=True)
