from taipan.Logging.Logger import Logger
from taipan.Learning.EntityIdentification.AgdistisTableIdentifier import AgdistisTableIdentifier

class SupportIdentifier(object):
    def __init__(self):
        self.logger = Logger().getLogger(__name__)
        self.agdistis = AgdistisTableIdentifier()

    def calculateSupport(self, entities):
        """
            support -- percentage of entities to occur in a column to be considered a candidate for a subject column (columns without entities are not subject column per definition)
        """
        numberOfColumns = len(entities[0])
        numberOfRows = len(entities)
        supports = [0]*numberOfColumns
        for rowIndex, entityRow in enumerate(entities):
            for columnIndex, entity in enumerate(entityRow):
                if(len(entity) > 0):
                    supports[columnIndex] += 1

        for columnIndex, columnScore in enumerate(supports):
            supports[columnIndex] = float(columnScore) / numberOfRows * 100

        return supports

    def identifySubjectColumn(self, table, support):
        entities = self.agdistis.disambiguateTable(table)
        supports = self.calculateSupport(entities)
        #Return column with maximum support 
        return supports.index(max(supports))
