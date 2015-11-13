from flask.ext.wtf import Form
from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired

class SubjectColumnAnnotatorForm(Form):
    subjectColumn = TextField('Subject Column Number [0-based]')
    noSubjectColumn = BooleanField('No Subject Column!')
    #tableType = SelectMultipleField('Table Type', choices=["Normal", "Vertical", "Layout", "Not English"])
    tableType = RadioField('Table Type', default="Normal", choices=[("Normal","Normal"), ("Layout", "Layout"), ("Vertical", "Vertical"), ("NotEnglish", "Not English"), ("Statistical", "Statistical")])
