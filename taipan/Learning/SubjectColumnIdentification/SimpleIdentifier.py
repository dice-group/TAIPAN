from taipan.Logging.Logger import Logger
from taipan.Utils.Exceptions import SubjectColumnNotFoundError

class SimpleIdentifier(object):
    """
        According to Recovering Semantics of Tables on The Web, 2011
        This should have precision of 83%
    """
    identificationThreshold = 0.1

    def __init__(self):
        self.logger = Logger().getLogger(__name__)

    def identifySubjectColumn(self, table):
        headerPosition = table.getHeaderPosition()
        relations = table.getTable()
        if(headerPosition != "FIRST_ROW"):
            self.logger.debug("Table has to be transposed!")
            self.logger.debug("%s"%(relations,))
            relations = relations.T

        for columnNumber, column in enumerate(relations):
            columnString = ''.join([element for element in column])
            digitsInString = 0
            for character in columnString:
                if character.isdigit():
                    digitsInString = digitsInString + 1
            digitsRatio = float(digitsInString)/len(columnString)
            if(digitsRatio < self.identificationThreshold):
                self.logger.debug("Subject column identified: %s" %(columnNumber,))
                self.logger.debug("%s" %(column,))
                return columnNumber

        raise SubjectColumnNotFoundError("SimpleIdentifier could not find subject column")
