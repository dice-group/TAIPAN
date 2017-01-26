# Load table into internal datastructure
from taipan.Generic.Table import Table
tableFilename = "test.csv"
_table = Table(tableFilename)

# Get subject column identification model
from taipan.Learning.SubjectColumnIdentification.Supervised.SupervisedIdentifier import SupervisedIdentifier
scIdentifier = SupervisedIdentifier()

# Identify subject column
subject_column = scIdentifier.identifySubjectColumn(_table)
_table.subjectColumn = subject_column[0]

# Get table properties
from taipan.Learning.PropertyMapping.RankedLovPropertyMapper import RankedLovPropertyMapper
propertyMapper = RankedLovPropertyMapper(scoreThreshold=0.6)
(properties, allproperties) = propertyMapper.mapProperties(_table)

import ipdb; ipdb.set_trace()
