import os
try:
   import cPickle as pickle
except:
   import pickle
import collections
from collections import Counter
import time

from taipan.Utils.Exceptions import NoInstancesFoundError
from taipan.Logging.Logger import Logger
from taipan.Config.Pathes import cacheFolder
from taipan.Utils.Exceptions import RelationsDataStructureNotFound
from taipan.Learning.SubjectColumnIdentification.DistantSupervisionIdentifier import DistantSupervisionIdentifier
from taipan.Learning.EntityIdentification.AgdistisIdentifier import AgdistisIdentifier
from taipan.Search.PropertySearch import PropertySearchDbpediaSparql

from SPARQLWrapper import SPARQLWrapper, JSON
from taipan.Config.ExternalUris import dbpediaSparqlEndpointUri

class SimplePropertyMapper(object):
    def __init__(self):
        self.logger = Logger().getLogger(__name__)
        self.agdistisIdentifier = AgdistisIdentifier()
        self.dbpediaSparql = SPARQLWrapper(dbpediaSparqlEndpointUri)
        self.dbpediaSparql.setReturnFormat(JSON)
        self.propertySearch = PropertySearchDbpediaSparql()

    def parseResults(self, results, variableName="property"):
        """
            Refactor in a separate class
        """
        properties = []
        for result in results:
            properties.append(result[variableName]['value'])
        return properties

    def getClassForEntity(self, entity):
        """
            Refactor in a separate class
        """
        self.dbpediaSparql.setQuery(u"""
            SELECT DISTINCT ?class
            WHERE {
                <%s> a ?class .
            }
        """ % (entity,))
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        return self.parseResults(results, variableName="class")

    def getEntities(self, tableId):
        entitiesCacheFile = os.path.join(cacheFolder, tableId + ".entities.cache")
        if os.path.exists(entitiesCacheFile):
            return pickle.load(open(entitiesCacheFile, 'rb'))
        else:
            raise EntitiesDataStructureNotFound("Entities data structure not available. Did you run subject column identification?")

    def getEntitiesWithClasses(self, tableId):
        entities = self.getEntities(tableId)
        entitiesWithClassesCache = os.path.join(cacheFolder, tableId + ".entities.with.classes.cache")
        if os.path.exists(entitiesWithClassesCache):
            entities = pickle.load(open(entitiesWithClassesCache, 'rb'))
        else:
            for rowIndex, entityRow in enumerate(entities):
                for columnIndex, entity in enumerate(entityRow):
                    for entityIndex, _entity in enumerate(entity):
                        entity[entityIndex] = (self.getClassForEntity(_entity), _entity)
            pickle.dump(entities, open(entitiesWithClassesCache, "wb" ) )
        return entities

    def getClasses(self, entities, numberOfColumns):
        classes = [[]]*numberOfColumns
        for rowIndex, entityRow in enumerate(entities):
            for columnIndex, entity in enumerate(entityRow):
                for entityIndex, _entity in enumerate(entity):
                    (_class, entityUrl) = _entity
                    try:
                        classes[columnIndex].append(_class)
                    except BaseException as e:
                        print("%s" % (str(e),))
        return classes

    def getMainClassForSubjectColumn(self, classes, subjectColumn):
        classesSubjectColumn = [item for sublist in classes[subjectColumn] for item in sublist]
        try:
            classCount = len(classesSubjectColumn)
            (mainClass, mainClassCount) = Counter(classesSubjectColumn).most_common(1)[0]
            mainClassScore = float(mainClassCount) / classCount * 100
        except IndexError:
            self.logger.debug("Main class could not be identified")
            mainClass = ""
        return mainClass

    def filterNonMainClassEntities(self, entities, mainClass, subjectColumn):
        for rowIndex, entityRow in enumerate(entities):
            for columnIndex, entity in enumerate(entityRow):
                if columnIndex != subjectColumn:
                    continue
                for entityIndex, _entity in enumerate(entity):
                    (_class, entityUrl) = _entity
                    if not mainClass in _class:
                        entities[rowIndex][columnIndex][entityIndex] = (None, None)
        return entities

    def findProperties(self, tableId, tableData, entities, subjectColumn, nonSubjectColumns):
        propertyCache = os.path.join(cacheFolder, tableId + ".property.star.cache")
        properties = collections.defaultdict(dict)
        if os.path.exists(propertyCache):
            properties = pickle.load(open(propertyCache, 'rb'))
        else:
            for rowIndex, entityRow in enumerate(entities):
                for columnIndex, entity in enumerate(entityRow):
                    if columnIndex != subjectColumn:
                        continue
                    if len(entity) <= 0:
                        continue
                    for entityIndex, _entity in enumerate(entity):
                        (_class, entityUrl) = _entity
                        if entityUrl != None:
                            for nonSubjectColumn in nonSubjectColumns:
                                cellValue = tableData[rowIndex][nonSubjectColumn]
                                properties[rowIndex][nonSubjectColumn] = self.propertySearch.uriLiteralSearch(entityUrl,cellValue)
            pickle.dump(properties, open(propertyCache, "wb" ) )
        return properties

    def aggregateProperties(self, properties, nonSubjectColumns):
        propertiesAggregate = collections.defaultdict(dict)
        for nonSubjectColumn in nonSubjectColumns:
            propertiesAggregate[nonSubjectColumn] = []
        for row in properties:
            for nonSubjectColumn in nonSubjectColumns:
                    propertiesAggregate[nonSubjectColumn].append(properties[row][nonSubjectColumn])

        for nonSubjectColumn in nonSubjectColumns:
            propertiesAggregate[nonSubjectColumn] = [item for sublist in propertiesAggregate[nonSubjectColumn] for item in sublist]

        return propertiesAggregate

    def getTopProperties(self, propertiesAggregate, nonSubjectColumns, threshold):
        topProperties = []
        for nonSubjectColumn in nonSubjectColumns:
            try:
                (topProperty, support) = Counter(propertiesAggregate[nonSubjectColumn]).most_common(1)[0]
                #In percents
                support = (float(support) / len(propertiesAggregate[nonSubjectColumn])) * 100
                if support > threshold:
                    topProperties.append({"uri": topProperty,
                     "columnIndex": nonSubjectColumn})
            except IndexError:
                self.logger.debug("No property identified for column %s"%(nonSubjectColumn))
        return topProperties

    def calculateScores(self, propertiesAggregate, nonSubjectColumns):
        scores = collections.defaultdict(dict)
        for nonSubjectColumn in nonSubjectColumns:
            scores[nonSubjectColumn] = []

        for nonSubjectColumn in nonSubjectColumns:
            scores[nonSubjectColumn] = Counter(propertiesAggregate[nonSubjectColumn])

        return scores

    def getScores(self, table, rowsToDisambiguate=20, threshold=10, support=0, connectivity=0):
        tableData = table.getData()
        tableHeader = table.getHeader()
        tableId = table.id
        numberOfRows = len(tableData[0]) #first column
        numberOfColumns = len(tableHeader)
        subjectColumn = table.subjectColumn
        if subjectColumn == None or subjectColumn == -1:
            return []

        nonSubjectColumns = [i for i in range(0,numberOfColumns)]
        nonSubjectColumns.remove(subjectColumn)

        self.logger.debug("Identifying properties for a table %s"%(tableId))

        entities = self.getEntitiesWithClasses(tableId)
        classes = self.getClasses(entities, numberOfColumns)
        mainClass = self.getMainClassForSubjectColumn(classes, subjectColumn)
        entities = self.filterNonMainClassEntities(entities, mainClass, subjectColumn)
        properties = self.findProperties(tableId, tableData, entities, subjectColumn, nonSubjectColumns)
        propertiesAggregate = self.aggregateProperties(properties, nonSubjectColumns)
        propertyScores = self.calculateScores(propertiesAggregate, nonSubjectColumns)

        return propertyScores

    def mapProperties(self, table, rowsToDisambiguate=20, threshold=10, support=0, connectivity=0):
        tableData = table.getData()
        tableHeader = table.getHeader()
        tableId = table.id
        numberOfRows = len(tableData)
        numberOfColumns = len(tableData[0])
        subjectColumn = table.subjectColumn
        if subjectColumn == None or subjectColumn == -1:
            return []

        nonSubjectColumns = [i for i in range(0,len(tableData[0]))]
        nonSubjectColumns.remove(subjectColumn)

        self.logger.debug("Identifying properties for a table %s"%(tableId))

        entities = self.getEntitiesWithClasses(tableId)
        classes = self.getClasses(entities, numberOfColumns)
        mainClass = self.getMainClassForSubjectColumn(classes, subjectColumn)
        entities = self.filterNonMainClassEntities(entities, mainClass, subjectColumn)
        properties = self.findProperties(tableId, tableData, entities, subjectColumn, nonSubjectColumns)
        propertiesAggregate = self.aggregateProperties(properties, nonSubjectColumns)
        propertyScores = self.calculateScores(propertiesAggregate, nonSubjectColumns)

        topProperties = self.getTopProperties(propertiesAggregate, nonSubjectColumns, threshold)

        return topProperties
