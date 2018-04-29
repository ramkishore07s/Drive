'''main page controllers'''
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

MAIN = Blueprint('main', __name__, template_folder='templates')

# ---------------------------- helper functions -------------------------------

def current_directory():
    return APP.config["UPLOAD_FOLDER"] + session["current_dir"]

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def set_cur_dir(dir_name):
    if dir_name == ".":
        session["current_dir"] = "/" + str(current_user.id)
    elif dir_name == "..":
        rem = session["current_dir"].split("/")
        if len(rem) > 0:
            rem.pop()
        session["current_dir"] = ""
        for file in rem[1:]:
            session["current_dir"] += "/" + file
    elif dir_name != "":
        session["current_dir"] += "/" + dir_name

    # protection, if tries to go back
    
    if len(session["current_dir"]) <= 1:
        session["current_dir"] = "/" + str(current_user.id)

@MAIN.context_processor
def user_auth():
    def is_logged_in():
        return current_user.is_authenticated
    return dict(is_logged_in=is_logged_in)

# ----------------------------- main view --------------------------------

@MAIN.route('/mydrive')
def show():
    '''show'''
    if current_user.is_authenticated:
        if not "current_dir" in session:
            session["current_dir"] = "/" + str(current_user.id)
        return render_template("main.html",
                               u_form=UploadFile(),
                               d_form=CreateDir(),
                               cd_form=ChangeDir())
    return redirect("/login")

# -------------------------- upload files to the current directory -------------------

@MAIN.route('/upload', methods=['POST'])
def upload_file():
    '''upload file in current directory'''
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_directory(), filename))
    else:
        flash("error uploading file")
    return redirect("mydrive")


# --------------------------- create dir in current directory -----------------
#
# creates dir in the current directory
# functionalities might depend on os

@MAIN.route('/makedir', methods=['POST'])
def create_dir():
    '''create dir in current dir'''
    form = CreateDir(request.form)
    if form.validate_on_submit():
        dir_name = form.dir_name.data
        try:
            if not dir_name == 'public':
                os.makedirs(current_directory() + "/" + dir_name)
            else:
                flash('The name is reserved')
                raise OSError('reserved name')
        except OSError:
            flash("Cannot create dir")
    else:
        flash("form error")
    return redirect("mydrive")


# ----------------------------- get files method ------------------------
#
# returns a list of files and folders and their sizes
# only of current directory
# Folder size is not calculated recursively, might add in future


@MAIN.route('/getFiles', methods=['GET'])
def get_files():
    files = []
    file_size = []
    folders = []
    folder_size = []
    if current_user.is_authenticated:

        # load files and folder names and sizes into lists
        
        for file in os.listdir(current_directory()):
            path = current_directory() + "/" + file
            if file != ".DS_Store":
                if os.path.isfile(path):
                    files.append(file)
                    file_size.append(os.stat(path).st_size)
                if os.path.isdir(path):
                    folders.append(file)
                    folder_size.append(get_size(path))

        # convert everything to json dumps

        files = json.dumps(files)
        file_size = json.dumps(file_size)
        folders = json.dumps(folders)
        folder_size = json.dumps(folder_size)
            
        return jsonify(files=files,
                       file_size=file_size,
                       folders=folders,
                       folder_size=folder_size)    
    else:
        return redirect("/login")


# ----------------------------- change dir ------------------------------

# .. => go back
# . => root folder of user
# other names => cd if exists
# send post request with json containing "change_dir":"<directory name>"

@MAIN.route('/changedir', methods=['POST'])
def change_dir():
    if current_user.is_authenticated:
        dir_name = request.json["change_dir"]
        if (dir_name == ".." or dir_name == "." 
            or dir_name in os.listdir(current_directory())) and os.path.isdir(current_directory() + "/" + dir_name):
            set_cur_dir(dir_name)
            return jsonify(result="success",
                           direc=str(session["current_dir"]),
                           cur=current_directory())
    else:
        return jsonify(result="failed")
    
    
# ------------------------ get particular file --------------------------

@MAIN.route('/getfile/<filename>', methods=['GET'])
def get_file(filename):
    if current_user.is_authenticated:
        abs_name = current_directory() + "/" + filename
        if filename in os.listdir(current_directory()) and os.path.isfile(abs_name):
            return send_from_directory(current_directory(), filename)
    else:
        return render_template("404.html")


# -------------------------- delete file --------------------------------
#
# post json with field { "del_file": <file/folder>
#

@MAIN.route('/delete', methods=['POST'])
def delete_file():
    if current_user.is_authenticated:
        try:
            filename = request.json["del_file"]
            print(filename)
            abs_path = current_directory() + "/" + filename
            if filename in os.listdir(current_directory()):
                if os.path.isfile(abs_path):
                    os.unlink(current_directory() + "/" + filename)
                elif os.path.isdir(abs_path) and not filename == 'public':
                    shutil.rmtree(abs_path)
                else:
                    return jsonify(result='failed')
                return jsonify(result="success")
            return jsonify(result="failed")
        except:
            return jsonify(result="failed")
    return redirect("login")
