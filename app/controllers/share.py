import os
import sys
import shutil

from flask import Blueprint, render_template, redirect, flash, request,\
    session, jsonify, json, send_file, send_from_directory
from flask_login import current_user
from werkzeug.utils import secure_filename

from jinja2 import TemplateNotFound

from app import DB, APP

from app.models.user import User

from app.controllers.forms.main import UploadFile, CreateDir, ChangeDir

SHARED = Blueprint('shared', __name__, template_folder='templates')

def set_cur_dir(dir_name):
    if( dir_name == '..'):
        rem = session['current_dir'].split('/').pop()
        session['current_dir'] = ""
        for s in rem[1:-1]:
            session['current_dir'] += '/' + s
    elif dir_name == '.':
        session['current_dir'] = ''
    else:
        abs_path = session['root'] + session['current_dir'] + '/' + dir_name
        if os.path.isdir(abs_path):
            session['current_dir'] += '/' + dir_name

@SHARED.context_processor
def user_auth():
    def is_logged_in():
        return current_user.is_authenticated
    return dict(is_logged_in=is_logged_in)


@SHARED.route('/shared/<user>/')
def current_user_dir(user):
    try:
        session['user_dir'] = int(user)
        session['root'] = APP.config['SHARED_FOLDER'] + '/' + str(user)
        session['current_dir'] = ""
        return render_template('shared.html')
    except:
        return render_template('404.html')


@SHARED.route('/blog/<int:user>', methods=['GET'])
def user_blog(user):
    id = str(user)
    filename = id + '/' + 'blog.html'
    print(os.listdir(APP.config['UPLOAD_FOLDER'] + '/' + id))
    print(APP.config['UPLOAD_FOLDER'] + '/' + id + '/blog.html')
    if 'blog.html' in os.listdir(APP.config['UPLOAD_FOLDER'] + '/' + id):
        return send_from_directory(APP.config['UPLOAD_FOLDER'] + '/' + id , 'blog.html')
    else:
        return render_template('404.html')

    
