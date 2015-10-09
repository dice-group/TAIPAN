import collections
import re
import taipan.Config.Pathes
import foxpy.fox
from taipan.Search.PropertySearch import PropertySearchDbpediaSparql

from taipan.Utils.Exceptions import SubjectColumnNotFoundError

from taipan.Logging.Logger import Logger

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

class DistantSupervisionIdentifier(object):
    def __init__(self):
        self.logger = Logger().getLogger(__name__)

    def identifySubjectColumn(self, table):
        tableData = table.getData()
        tableHeader = table.getHeader()

        relations = collections.defaultdict(dict)
        entities = []
        for row in tableData:
            entities = self.identifyEntitiesForRow(row, tableHeader)
            for itemIndex, entity in enumerate(entities):
                item = row[itemIndex]
                for otherItemIndex, otherItem in enumerate(row[itemIndex:]):
                    if(row[itemIndex] == row[otherItemIndex]):
                        relations[itemIndex][otherItemIndex] = []
                    else:
                        rel = self.findRelation(item, otherItem, entities[itemIndex], entities[otherItemIndex])
                        relations[itemIndex][otherItemIndex] = rel
                        relations[otherItemIndex][itemIndex] = rel

        import ipdb; ipdb.set_trace()
        return 0

    def findRelation(self, columnValue1, columnValue2, entity1, entity2):
        propertySearch = PropertySearchDbpediaSparql()
        properties = []
        if(entity1 != ''):
            properties = propertySearch.uriLiteralSearch(entity1,columnValue2)
        elif(entity2 != ''):
            properties = propertySearch.uriLiteralSearch(entity2,columnValue1)
        elif(entity1 != '' and entity2 != ''):
            properties = propertySearch.uriUriSearch(entity1, entity2)
        else:
            properties = []
        return properties

    def identifyEntitiesForRow(self, row, tableHeader):
        entities = []
        for itemIndex, item in enumerate(row):
            entities.append(self.identifyEntity(item, tableHeader[itemIndex]))
        return entities

    def identifyEntity(self, columnValue, headerValue):
        fx = foxpy.fox.Fox()
        (text, output, log) = fx.recognizeText(
                self.clearString(headerValue) + ' ' + self.clearString(columnValue))
        #grab dbpedia:.* from output
        entity = re.search("\"(dbpedia:.*)\"", output)
        if(entity):
            entity = entity.group(1)
            entity = re.sub('dbpedia:', "http://dbpedia.org/resource/", entity)
            print entity
            return entity
        else:
            return ""

    def clearString(self, string):
        characters = "{}|"
        string = string.translate(None, characters)
        string = re.sub('&nbsp;', '', string)
        string = string.strip()
        print string
        return string

class SVMIdentifier(object):
    """
        According to Recovering Semantics of Tables on The Web, 2011
        should have precision of 94%
        Features to use:
        - Fraction of cells with unique content
        - Fraction of cells with numeric content
        - Variance in the number of date tokens in each cell
        - Average number of words in each cell
        - Column index from left
    """
    def __init__(self):
        pass
