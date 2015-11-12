from app import app
from flask import render_template, abort, redirect, url_for

from forms import SubjectColumnAnnotatorForm

from TableSelector.SubjectColumnTableSelector import SubjectColumnTableSelector
from model import GoogleSpreadsheet

@app.route('/')
def index():
    #TODO: get random table id group from database
    return redirect(url_for('annotateSubjectColumn', username="ivan"))

@app.route('/table/<path:tableId>')
def table(tableId):
    return "%s" % (tableId,)

@app.route('/table/annotateSubjectColumn/<username>')
def annotateSubjectColumn(username):
    form = SubjectColumnAnnotatorForm()
    gSpread = GoogleSpreadsheet()
    worksheet = gSpread.createOrGetNamedWorksheet(username)
    tableSelector = SubjectColumnTableSelector()
    table = tableSelector.getRandomTable()
    import ipdb; ipdb.set_trace()
    return render_template("annotateSubjectColumn.html", form=form, table=table)
    #return "%s" % (tableGroupId,)
