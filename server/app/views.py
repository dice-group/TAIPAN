from app import app
from flask import render_template, abort, redirect, url_for

from forms import SubjectColumnAnnotatorForm

from TableSelector.SubjectColumnTableSelector import SubjectColumnTableSelector

@app.route('/')
def index():
    #TODO: get random table id group from database
    return redirect(url_for('annotateSubjectColumn', tableGroupId="fodisjf"))

@app.route('/table/<path:tableId>')
def table(tableId):
    return "%s" % (tableId,)

@app.route('/table/annotateSubjectColumn/<path:tableGroupId>')
def annotateSubjectColumn(tableGroupId):
    form = SubjectColumnAnnotatorForm()
    tableSelector = SubjectColumnTableSelector()
    table = tableSelector.getRandomTable()
    return render_template("annotateSubjectColumn.html", form=form, table=table)
    #return "%s" % (tableGroupId,)
