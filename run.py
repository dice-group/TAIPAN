
from taipan.Learning.SubjectColumnIdentification.Supervised.SupervisedIdentifier import SupervisedIdentifier

tableFilename = "test.csv"
#table = load table
#necessary functionality for subject identification:
#* decouple following functions from T2DTable
#* table.getData
#* table.getHeader

DecisionTreeClassifierID = 4
scIdentifier = SupervisedIdentifier(DecisionTreeClassifierID)
scIdentifier.identifySubjectColumn(table)
