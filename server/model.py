from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from tableapp import app

db = SQLAlchemy(app)

class AnnotatedTable(db.Model):
    __tablename__ = "annotatedtable"
    id = db.Column('id', db.Integer, primary_key=True)
    tableId = db.Column('tableId', db.Unicode)
    subjectColumn = db.Column('subjectColumn', db.Integer)
    comment = db.Column('comment', db.Unicode)
    annotatedAt = db.Column('annotatedAt', db.Date, default=datetime.utcnow)

def addTable(tableId, subjectColumn, comment):
    t = AnnotatedTable(tableId=tableId, subjectColumn=int(subjectColumn), comment=comment)
    db.session.add(t)
    db.session.commit()
