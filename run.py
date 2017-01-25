# Load table into internal datastructure
from taipan.Generic.Table import Table
tableFilename = "test.csv"
_table = Table(tableFilename)

# Get subject column identification model
from taipan.Learning.SubjectColumnIdentification.Supervised.SupervisedIdentifier import SupervisedIdentifier
scIdentifier = SupervisedIdentifier()
subject_column = scIdentifier.identifySubjectColumn(_table)
import ipdb; ipdb.set_trace()
