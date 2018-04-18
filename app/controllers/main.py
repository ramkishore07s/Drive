'''main page controllers'''
import os

from flask import Blueprint, render_template, redirect, flash, request,\
    session, jsonify, json
from flask_login import current_user
from werkzeug.utils import secure_filename

from jinja2 import TemplateNotFound

from app import DB, APP

from app.models.user import User

from app.controllers.forms.main import UploadFile, CreateDir, ChangeDir

MAIN = Blueprint('main', __name__, template_folder='templates')

# ---------------------------- helper functions -------------------------------

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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


# ----------------------------- main view --------------------------------

@MAIN.route('/mydrive')
def show():
    '''show'''
    if current_user.is_authenticated:
        if not "current_dir" in session:
            session["current_dir"] = "/" + str(current_user.id)
        flash(current_directory())
        return render_template("main.html",
                               u_form=UploadFile(),
                               d_form=CreateDir(),
                               cd_form=ChangeDir())
    return redirect("/login")

# -------------------------- upload files to the current directory -------------------

@MAIN.route('/upload', methods=['POST'])
def upload_file():
    '''upload file in current directory'''
    form = UploadFile(request.form)
    if form.validate_on_submit():
        flash(str(request.files['file_'].filename))
        file = request.files['file_']
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_directory(), filename))
    else:
        flash("error")
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
        flash(form.dir_name.data)
        dir_name = form.dir_name.data
        try:
            os.makedirs(current_directory() + "/" + dir_name)
        except OSError:
            flash("cannot create dir")
    else:
        flash("error cd")
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


# Accepts a json post request with field change_dir = directory name
# ''' example request:
# var xhr = new XMLHttpRequest();
# var url = "/changedir";
# xhr.open("POST", url, true);
# xhr.setRequestHeader("Content-Type", "application/json");
# xhr.onreadystatechange = function () {
#     if (xhr.readyState === 4 && xhr.status === 200) {
#         var json = JSON.parse(xhr.responseText);
#         console.log(json);
#     }
# };
# var data = JSON.stringify({"change_dir":"documents"});
# xhr.send(data);
# '''

# add back function

@MAIN.route('/changedir', methods=['POST'])
def change_dir():
    dir_name = request.json["change_dir"]
    if dir_name == ".." or dir_name == "." or dir_name in os.listdir(current_directory()):
        set_cur_dir(dir_name)
        return jsonify(result="success",
                       direc=str(session["current_dir"]),
                       cur=current_directory())
    else:
        return jsonify(result="failed")
