from taipan.Learning.SubjectColumnIdentification import SimpleIdentifier
from taipan.Utils.Exceptions import SubjectColumnNotFoundError

class MannheimAtomizer(object):
    """
        Atomizes table based on subject column into N
        tables, where N is (number of columns - 1)
    """
    def __init__(self):
        self.subjectColumnIdentifier = SimpleIdentifier()

    def atomizeTable(self, table):
        try:
            subjectColumn = self.subjectColumnIdentifier.identifySubjectColumn(table)
        except SubjectColumnNotFoundError as e:
            print("Subject column not found %s" %(str(e),))
            subjectColumn = 0
        relations = table.getTable()
        atomicTables = []
        for index in range(subjectColumn, len(relations) - 1):
            atomicTable = relations[subjectColumn:subjectColumn+index+2:index+1]
            atomicTables.append(atomicTable)
        return atomicTables
