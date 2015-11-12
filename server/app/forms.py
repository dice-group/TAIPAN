from flask.ext.wtf import Form
from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField
from wtforms.validators import DataRequired

class SubjectColumnAnnotatorForm(Form):
    subjectColumn = TextField('Subject Column Number [0-based]')
    noSubjectColumn = BooleanField('No Subject Column!')
