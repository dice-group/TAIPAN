#!/usr/bin/python

import sys

tableId = sys.argv[1]
from taipan.T2D.Table import T2DTable
table = T2DTable(tableId)
from taipan.Learning.SubjectColumnIdentification.DistantSupervisionIdentifier import DistantSupervisionIdentifier
dlIdentifier = DistantSupervisionIdentifier()
subjectColumn = dlIdentifier.identifySubjectColumn(table)
print subjectColumn
print table.properties
print table.classes
print table.getData()[0:2]
print table.table
