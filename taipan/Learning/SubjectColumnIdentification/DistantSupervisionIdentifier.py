try:
   import cPickle as pickle
except:
   import pickle
import collections
import re
import os
import operator
import time

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

    def identifySubjectColumn(self, table, rowsToAnalyze=20, rowsFromCache=None):
        #limit to 20 rows for analysis
        tableData = table.getData()
        tableHeader = table.getHeader()
        tableId = table.id
        cacheFile = os.path.join(cacheFolder, tableId + ".relations.cache")
        self.logger.debug(tableId)

        self.executionStartTimePoint = 0
        self.executionEndTimePoint = 0
        self.executionTimeFull = 0
        self.executionTimePure = 0 #without querying and disambiguation
        self.queryTime = 0
        self.agdistisTime = 0

        self.executionStartTimePoint = time.time()
        if(os.path.exists(cacheFile)):
            relations = pickle.load(open(cacheFile, 'rb'))
            if rowsFromCache != None:
                relations = relations[:rowsFromCache]
        else:
            relations = []
            entities = []
            for row in tableData[:rowsToAnalyze]:
                rowRels = collections.defaultdict(dict)

                agdistisStartTimePoint = time.time()
                entities = self.identifyEntitiesForRow(row, tableHeader)
                agdistisEndTimePoint = time.time()
                agdistisTimeForARow = agdistisEndTimePoint - agdistisStartTimePoint
                self.agdistisTime += agdistisTimeForARow

                for itemIndex, item in enumerate(row):
                    entity = entities[itemIndex]
                    for otherItemIndex, otherItem in enumerate(row[itemIndex:]):
                        otherItemIndex = itemIndex + otherItemIndex
                        if(row[itemIndex] == row[otherItemIndex]):
                            rowRels[itemIndex][otherItemIndex] = []
                        else:
                            rel = self.findRelation(item, otherItem, entities[itemIndex], entities[otherItemIndex])
                            rowRels[itemIndex][otherItemIndex] = rel
                            rowRels[otherItemIndex][itemIndex] = rel
                relations.append(dict(rowRels))
                #save cache
            pickle.dump(relations, open(cacheFile, "wb" ) )

        subjectColumns = []
        for relation in relations:
            scores = collections.defaultdict(dict)
            for column in relation:
                score = 0
                for otherColumn in relation[column]:
                    score += len(relation[column][otherColumn])
                scores[column] = score

            maximum = max(scores.iteritems(), key=operator.itemgetter(1))[0]
            subjectColumns.append(maximum)

        from collections import Counter
        subjectColumn = Counter(subjectColumns).most_common(1)[0][0]

        self.executionEndTimePoint = time.time()
        self.executionTimeFull = self.executionEndTimePoint - self.executionStartTimePoint
        self.executionTimePure = self.executionTimeFull - self.queryTime - self.agdistisTime

        return subjectColumn

    def findRelation(self, columnValue1, columnValue2, entities1, entities2):
        propertySearch = PropertySearchDbpediaSparql()
        properties = []

        executionQueryStart = time.time()
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

        executionQueryEnd = time.time()
        executionQueryTime = executionQueryEnd - executionQueryStart
        self.queryTime += executionQueryTime

        #flatten
        properties = [prop for sublist in properties for prop in sublist]
        #remove duplicates
        properties = list(set(properties))

        return properties

    def identifyEntitiesForRow(self, row, tableHeader):
        entities = []
        for itemIndex, item in enumerate(row):
            rowEntities = self.agdistisIdentifier.identifyEntity(item)
            entities.append(self.agdistisIdentifier.flattenUrls(rowEntities))
        self.logger.debug("Entities found: %s" %(entities))
        return entities
