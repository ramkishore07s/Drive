''' Public data and Blogs'''

# New:
# ====================================== Blogs ===========================================
#
# Blogs are static page for each user.
# 'blog.html' located in root directory of each user will be server under '/blog/<user id>'
# Currently only inline css and js are supported.
# Inspired by <username>.github.io feature

# ============================= Important Information ===================================
#
# 1. This controller does not use any form of authentication since it only
#     handles public data, and is visible to everyone.
# 2. Public data is any file stored in the 'public' folder in the root
#     directory of each user. Note that 'public' folders are not supported yet.
#    Only files in that folder will be visible to everyone.

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

# ================================= Not used anywhere ==================================
#
# For folder support in public files
# 

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


# ================================= used in html to display logout button ==============
            
@SHARED.context_processor
def user_auth():
    def is_logged_in():
        return current_user.is_authenticated
    return dict(is_logged_in=is_logged_in)

@SHARED.route('/shared')
def shared():
    folders = []
    for file in os.listdir(APP.config['UPLOAD_FOLDER']):
        if not file == '.DS_Store':
            folders.append(file)
    print(len(folders))
    return render_template('shared_folders.html',
                           folders=folders,
                           length={"length":len(folders)})

# ========================== show public files of particular user ======================

@SHARED.route('/shared/<int:user>/')
def current_user_dir(user):
    session['user_dir'] = int(user)
    session['root'] = APP.config['UPLOAD_FOLDER'] + '/'+ str(user) + '/public/'
    session['current_dir'] = ""
    print(session['root'])
    files = []
    for file in os.listdir(session['root']):
        if os.path.isfile(session['root'] + '/' + file) and not file == '.DS_Store':
            files.append(file)
    return render_template('shared.html', files=files, user=user)

# ========================= show particular public file =============================

@SHARED.route('/shared/<int:user>/<filename>')
def get_file(user, filename):
    folder = APP.config['UPLOAD_FOLDER'] + '/' + str(user) + '/public/';
    file = filename
    if file in os.listdir(folder) and not file == '.DS_Store':
        return send_from_directory(folder, file)
    return render_template('404.html')


# =========================== show blog of user =========================================
#
# Only if the user has uploaded 'blog.html' in his root directory, else 404 is returned
#

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

    
