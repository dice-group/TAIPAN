import numpy

from taipan.Learning.SubjectColumnIdentification import SimpleIdentifier
from taipan.Utils.Exceptions import SubjectColumnNotFoundError
from taipan.Utils.Exceptions import CouldNotAtomizeError

from taipan.Logging.Logger import Logger

class MannheimAtomizer(object):
    """
        Atomizes table based on subject column into N
        tables, where N is (number of columns - 1)
    """
    def __init__(self):
        self.subjectColumnIdentifier = SimpleIdentifier()
        self.logger = Logger().getLogger(__name__)

    def atomizeTable(self, table):
        try:
            subjectColumnNumber = self.subjectColumnIdentifier.identifySubjectColumn(table)
        except SubjectColumnNotFoundError as e:
            self.logger.error("Subject column not found", exc_info=True)
            subjectColumnNumber = 0
        relations = table.getTable()
        atomicTables = []
        subjectCol = relations[subjectColumnNumber]
        for index in range(len(relations) - 1):
            if index != subjectColumnNumber:
                otherCol = relations[index]
                atomicTable = numpy.array([subjectCol, otherCol])
                atomicTables.append(atomicTable)
            else:
                continue
        if(len(atomicTables) < 1):
            raise CouldNotAtomizeError("Table could not be atomized!")
            self.logger.error("Table could not be atomized!")
            self.logger.error("%s" % (relations,))
        return atomicTables
