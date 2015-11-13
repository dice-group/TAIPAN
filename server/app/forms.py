from flask.ext.wtf import Form
from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField, RadioField, SelectMultipleField
from wtforms.validators import Required, Regexp

class SubjectColumnAnnotatorForm(Form):
    subjectColumn = TextField('Subject Column: <span class="label label-default" id="subjectColumnValue">Click to select</span>')
    noSubjectColumn = BooleanField('No Subject Column!')
    #tableType = SelectMultipleField('Table Type', choices=["Normal", "Vertical", "Layout", "Not English"])
    tableType = RadioField('Table Type', default="Normal", choices=[("Normal","Normal"), ("Layout", "Layout"), ("Vertical", "Vertical"), ("Statistical", "Statistical"), ("NotEnglish", "Not English")])

class UsernameForm(Form):
    username = TextField('Your name', [Regexp("^[a-zA-Z0-9_]*$", message="only alphanumerical usernames are allowed"), Required(message="please provide a username")])
