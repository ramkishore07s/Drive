from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField

class UploadFile(FlaskForm):
    file = FileField('file', validators=[DataRequired()])
    submit = SubmitField('Add file')

class CreateDir(FlaskForm):
    dir_name = StringField('Enter the Name of Folder to be created:', validators=[DataRequired()])
    submit = SubmitField('Create Directory')

class ChangeDir(FlaskForm):
    dir_name = StringField('Directory Name', validators=[DataRequired()])
    submit = SubmitField('Create Directory')
