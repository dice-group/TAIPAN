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
from taipan.Learning.EntityIdentification.AgdistisIdentifier import AgdistisIdentifier
import taipan.Config.Pathes

class DistantSupervisionIdentifier(object):
    def __init__(self):
        self.logger = Logger().getLogger(__name__)
        self.agdistisIdentifier = AgdistisIdentifier()

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

    def findRelation(self, columnValue1, columnValue2, entities1, entities2):
        propertySearch = PropertySearchDbpediaSparql()
        properties = []
        if(len(entities1) > 0):
            for entity1 in entities1:
                properties.append(propertySearch.uriLiteralSearch(entity1,columnValue2))
        elif(len(entities2) > 0):
            for entity2 in entities2:
                properties.append(propertySearch.uriLiteralSearch(entity2,columnValue1))
        elif(len(entities1) > 0 and len(entities2) > 0):
            for entity1 in entities1:
                for entity2 in entities2:
                    properties.append(propertySearch.uriUriSearch(entity1, entity2))
        else:
            #both are literals, do nothing
            pass

        #flatten
        properties = [prop for sublist in properties for prop in sublist]
        #remove duplicates
        properties = list(set(properties))

        import ipdb; ipdb.set_trace()

        return properties

    def identifyEntitiesForRow(self, row, tableHeader):
        entities = []
        for itemIndex, item in enumerate(row):
            rowEntities = self.agdistisIdentifier.identifyEntity(item)
            entities.append(self.agdistisIdentifier.flattenUrls(rowEntities))
        return entities
