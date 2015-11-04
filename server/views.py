from tableapp import app
from taipan.

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/table/<path:tableId>')
def table(tableId):
    return "%s" % (tableId,)
