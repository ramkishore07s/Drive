''' Init module '''
# ------------------------------------ Init module -------------------------------------------
#
# Handles app, db initilization, configuration, error handlers and blueprints
#

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

APP = Flask(__name__)

# ------------------------------- App configuration -----------------------------------------
#

APP.config.from_object(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'data')
SHARED_FOLDER = os.path.join(APP_ROOT, 'shared')

APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
APP.config['SHARED_FOLDER'] = SHARED_FOLDER
APP.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

APP.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    SESSION_COOKIE_PATH='/',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
))
APP.config.from_envvar('FLASKR_SETTINGS', silent=True)

DB = SQLAlchemy(APP)
LOGIN = LoginManager(APP)

# ------------------------------- controller imports -----------------------------------------
#
# Each of them is abstracted as blueprints specific to their tasks

from app.controllers.main import MAIN
from app.controllers.auth import AUTH
# Registering imported Blueprints

APP.register_blueprint(MAIN)
APP.register_blueprint(AUTH)


# ------------------------------- Initialising DB -------------------------------------------

DB.init_app(APP)
DB.create_all()

@APP.route('/')
def hello_world():
    '''hello world'''
    session['log'] = True
    if not session['log']:
        return render_template("app.html")
    else:
        session['log'] = not session['log']
        return "hellooo"

    return render_template("app.html")


# ------------------------------- error handlers ---------------------------------------------

@APP.errorhandler(404)
def page_not_found(_):
    '''404'''
    return render_template("404.html"), 404

if __name__ == '__main__':
    APP.run(debug=True)
