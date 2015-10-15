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
    """

    """

    def __init__(self):
        self.logger = Logger().getLogger(__name__)
        self.dlIdentifier = DistantSupervisionIdentifier()
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

    def mapProperties(self, table, rowsToDisambiguate=20, threshold=10):
        tableData = table.getData()
        tableHeader = table.getHeader()
        tableId = table.id
        subjectColumn = self.dlIdentifier.identifySubjectColumn(table)
        nonSubjectColumns = range(0,len(tableData[0]))
        nonSubjectColumns.remove(subjectColumn)
        self.logger.debug("Identifying properties for a table %s"%(tableId))

        self.executionTimeFull = 0
        self.executionTimePure = 0
        self.disambiguationTime = 0
        self.classSearchTime = 0
        self.propertySearchTime = 0

        startTime = time.time()

        #disambiguate entities
        disambiguationTimeStart = time.time()
        entitiesCacheFile = os.path.join(cacheFolder, tableId + ".entities.cache")
        entitySets = []
        if os.path.exists(entitiesCacheFile):
            entitySets = pickle.load(open(entitiesCacheFile, 'rb'))
        else:
            for row in tableData[:rowsToDisambiguate]:
                entitySets.append(self.agdistisIdentifier.identifyEntity(row[subjectColumn]))
            pickle.dump(entitySets, open(entitiesCacheFile, "wb" ) )

        disambiguationTimeEnd = time.time()
        self.disambiguationTime = disambiguationTimeEnd - disambiguationTimeStart

        ## get all classes for those
        ## take the most frequent one
        ## filter out all other disambiguations
        filteredEntitiesCache = os.path.join(cacheFolder, tableId + ".entities.filtered.cache")
        if os.path.exists(filteredEntitiesCache):
            entitySets = pickle.load(open(filteredEntitiesCache, 'rb'))
        else:
            classes = []
            classSearchTimeStart = time.time()
            for entitySet in entitySets:
                for entity in entitySet:
                    entity['classes'] = []
                    if entity['disambiguatedURL']:
                        entity['classes'] = self.getClassForEntity(entity['disambiguatedURL'])
                        classes.append(entity['classes'])
            classSearchTimeEnd = time.time()
            self.classSearchTime = classSearchTimeEnd - classSearchTimeStart
            #flatten classes
            classes = [item for sublist in classes for item in sublist ]
            #identify the main class for the subject column
            try:
                mainClass = Counter(classes).most_common(1)[0][0]
            except IndexError:
                self.logger.debug("Main class could not be identified")
                mainClass = ""

            for entitySet in entitySets:
                entitiesToRemove = []
                for index, entity in enumerate(entitySet):
                    if not mainClass in entity['classes']:
                        entitiesToRemove.append(index)
                for entityIndex in reversed(entitiesToRemove):
                    del entitySet[entityIndex]

            pickle.dump(entitySets, open(filteredEntitiesCache, "wb" ) )

        #find all properties for each entity-value pair
        properties = collections.defaultdict(dict)
        propertyCache = os.path.join(cacheFolder, tableId + ".property.star.cache")
        if os.path.exists(propertyCache):
            properties = pickle.load(open(propertyCache, 'rb'))
        else:
            propertySearchTimeStart = time.time()
            for rowIndex, entitySet in enumerate(entitySets):
                if entitySet == []:
                    continue
                entity = entitySet[0]['disambiguatedURL']
                if entity == "":
                    continue
                for nonSubjectColumn in nonSubjectColumns:
                    cellValue = tableData[rowIndex][nonSubjectColumn]
                    properties[rowIndex][nonSubjectColumn] = self.propertySearch.uriLiteralSearch(entity,cellValue)

            propertySearchTimeEnd = time.time()
            self.propertySearchTime = propertySearchTimeEnd - propertySearchTimeStart
            pickle.dump(properties, open(propertyCache, "wb" ) )

        #Aggregate properties for each atomic table
        propertiesAggregate = collections.defaultdict(dict)
        for nonSubjectColumn in nonSubjectColumns:
            propertiesAggregate[nonSubjectColumn] = []
        for row in properties:
            for nonSubjectColumn in nonSubjectColumns:
                propertiesAggregate[nonSubjectColumn].append(properties[row][nonSubjectColumn])

        #Flatten
        topProperties = []
        for nonSubjectColumn in nonSubjectColumns:
            propertiesAggregate[nonSubjectColumn] = [item for sublist in propertiesAggregate[nonSubjectColumn] for item in sublist]
            #And take top property
            try:
                (topProperty, support) = Counter(propertiesAggregate[nonSubjectColumn]).most_common(1)[0]
                #In percents
                support = (float(support) / len(propertiesAggregate[nonSubjectColumn])) * 100
                if support > threshold:
                    topProperties.append((topProperty,nonSubjectColumn))
            except IndexError:
                self.logger.debug("No property identified for column %s"%(nonSubjectColumn))

        endTime = time.time()
        self.executionTimeFull = endTime - startTime
        self.executionTimePure = self.executionTimeFull - self.disambiguationTime - self.classSearchTime - self.propertySearchTime

        #check if seed properties contain properties we are trying to find
        self.seedListContains = 0
        for _property in table.properties:
            if _property['uri'] in propertiesAggregate[_property['columnIndex']]:
                self.seedListContains += 1

        return topProperties
