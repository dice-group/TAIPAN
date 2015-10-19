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

    def identifySubjectColumn(self, table, rowsToAnalyze=20, rowsFromCache=None, subjectColumnEntitiesThreshold=80, subjectColumnRelationsThreshold=80):
        """
            rowsToAnalyze -- how many rows should be evaluated
            rowsFromCache -- can be used to reduce number of rows to be read from cache
            subjectColumnEntitiesThreshold -- percentage of entities to occur in a column to be considered a candidate for a subject column (columns without entities are not subject column per definition)
            subjectColumnRelationsThreshold -- percentage of subject columns identified inside the analyzed part of the table (divided by the total number of rows), i.e. 80% means that the same subject column identified for 80% of rows
        """
        tableData = table.getData()
        tableHeader = table.getHeader()
        tableId = table.id
        numberOfRows = len(tableData)
        numberOfColumns = len(tableData[0])

        cacheFileRelations = os.path.join(cacheFolder, tableId + ".relations.cache")
        cacheFileEntities = os.path.join(cacheFolder, tableId + ".entities.cache")
        self.logger.debug(tableId)

        self.executionStartTimePoint = 0
        self.executionEndTimePoint = 0
        self.executionTimeFull = 0
        self.executionTimePure = 0 #without querying and disambiguation
        self.queryTime = 0
        self.agdistisTime = 0

        self.executionStartTimePoint = time.time()
        #identify entities
        agdistisStartTimePoint = time.time()
        if(os.path.exists(cacheFileEntities)):
            entities = pickle.load(open(cacheFileEntities, 'rb'))
            if rowsFromCache != None:
                entities = entities[:rowsFromCache]
        else:
            entities = []
            for row in tableData[:rowsToAnalyze]:
                entitiesRow = self.identifyEntitiesForRow(row, tableHeader)
                entities.append(entitiesRow)
            #save cache
            pickle.dump(entities, open(cacheFileEntities, "wb" ) )

        agdistisEndTimePoint = time.time()
        self.agdistisTime = agdistisEndTimePoint - agdistisStartTimePoint

        #we consider only column which has at least 80% entities
        columnScores = [0]*numberOfColumns
        for rowIndex, entityRow in enumerate(entities):
            for columnIndex, entity in enumerate(entityRow):
                if(len(entity) > 0):
                    columnScores[columnIndex] += 1

        #Normalize
        for columnIndex, columnScore in enumerate(columnScores):
            columnScores[columnIndex] = float(columnScore) / numberOfRows * 100

        if(os.path.exists(cacheFileRelations)):
            relations = pickle.load(open(cacheFileRelations, 'rb'))
            if rowsFromCache != None:
                relations = relations[:rowsFromCache]
        else:
            relations = []
            for rowIndex, row in enumerate(tableData[:rowsToAnalyze]):
                rowRels = collections.defaultdict(dict)
                for itemIndex, item in enumerate(row):
                    entity = entitiesRow[itemIndex]
                    for otherItemIndex, otherItem in enumerate(row[itemIndex:]):
                        otherItemIndex = itemIndex + otherItemIndex
                        if(row[itemIndex] == row[otherItemIndex]):
                            rowRels[itemIndex][otherItemIndex] = []
                        else:
                            rel = self.findRelation(item, otherItem, entitiesRow[itemIndex], entitiesRow[otherItemIndex])
                            rowRels[itemIndex][otherItemIndex] = rel
                            rowRels[otherItemIndex][itemIndex] = rel
                relations.append(dict(rowRels))
            #save cache
            pickle.dump(relations, open(cacheFileRelations, "wb" ) )

        subjectColumns = []
        for relation in relations:
            scores = collections.defaultdict(dict)
            for column in relation:
                score = 0
                for otherColumn in relation[column]:
                    score += len(relation[column][otherColumn])
                scores[column] = score

            #remove non subject column
            for columnIndex, columnScore in enumerate(columnScores):
                if columnScore < subjectColumnEntitiesThreshold:
                    del scores[columnIndex]

            maximum = None
            if len(scores) > 0:
                maximum = max(scores.iteritems(), key=operator.itemgetter(1))[0]

            subjectColumns.append(maximum)

        subjectColumnScores = [0]*numberOfColumns
        for subjectColumn in subjectColumns:
            subjectColumnScores[subjectColumn] += 1

        #Normalize
        for columnIndex, subjectColumnScore in enumerate(subjectColumnScores):
            subjectColumnScores[columnIndex] = float(subjectColumnScore) / numberOfRows * 100

        subjectColumn = [columnIndex for columnIndex, columnScore in enumerate(subjectColumnScores) if columnScore >= subjectColumnRelationsThreshold]

        self.executionEndTimePoint = time.time()
        self.executionTimeFull = self.executionEndTimePoint - self.executionStartTimePoint
        self.executionTimePure = self.executionTimeFull - self.queryTime - self.agdistisTime

        if(len(subjectColumn) < 0):
            return None
        else:
            return subjectColumn[0]

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
