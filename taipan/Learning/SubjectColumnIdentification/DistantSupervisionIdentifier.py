try:
   import cPickle as pickle
except:
   import pickle
import collections
import re
import os

from taipan.Logging.Logger import Logger
from taipan.Utils.Exceptions import SubjectColumnNotFoundError
from taipan.Config.Pathes import cacheFolder
from taipan.Search.PropertySearch import PropertySearchDbpediaSparql
import taipan.Config.Pathes

class DistantSupervisionIdentifier(object):
    def __init__(self):
        self.logger = Logger().getLogger(__name__)

    def identifySubjectColumn(self, table):
        tableData = table.getData()
        tableHeader = table.getHeader()
        tableId = table.id
        cacheFile = os.path.join(cacheFolder, tableId + ".relations.cache")

        if(os.path.exists(cacheFile)):
            relations = pickle.load(open(cacheFile, 'rb'))
        else:
            relations = collections.defaultdict(dict)
            entities = []
            for row in tableData:
                entities = self.identifyEntitiesForRow(row, tableHeader)
                for itemIndex, item in enumerate(row):
                    entity = entities[itemIndex]
                    for otherItemIndex, otherItem in enumerate(row[itemIndex:]):
                        otherItemIndex = itemIndex + otherItemIndex
                        if(row[itemIndex] == row[otherItemIndex]):
                            relations[itemIndex][otherItemIndex] = []
                        else:
                            rel = self.findRelation(item, otherItem, entities[itemIndex], entities[otherItemIndex])
                            relations[itemIndex][otherItemIndex] = rel
                            relations[otherItemIndex][itemIndex] = rel
                #save cache
            pickle.dump(dict(relations), open(cacheFile, "wb" ) )

        scores = collections.defaultdict(dict)
        for column in relations:
            score = 0
            for otherColumn in relations[column]:
                score += len(relations[column][otherColumn])
            scores[column] = score

        import operator
        maximum = max(scores.iteritems(), key=operator.itemgetter(1))[0]

        return maximum

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
