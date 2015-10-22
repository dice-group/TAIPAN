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

    def mapProperties(self, table, rowsToDisambiguate=20, threshold=10, support=0, connectivity=0):
        tableData = table.getData()
        tableHeader = table.getHeader()
        tableId = table.id
        numberOfRows = len(tableData)
        numberOfColumns = len(tableData[0])
        subjectColumn = self.dlIdentifier.identifySubjectColumn(table)
        self.subjectColumn = subjectColumn
        self.subjectColumnCorrect = table.isSubjectColumn(subjectColumn)

        self.executionTimeFull = 0
        self.executionTimePure = 0
        self.disambiguationTime = 0
        self.classSearchTime = 0
        self.propertySearchTime = 0
        self.seedListContains = 0
        if subjectColumn == None:
            return []

        nonSubjectColumns = range(0,len(tableData[0]))
        nonSubjectColumns.remove(subjectColumn)

        entitiesCacheFile = os.path.join(cacheFolder, tableId + ".entities.cache")
        entitiesWithClassesCache = os.path.join(cacheFolder, tableId + ".entities.with.classes.cache")
        propertyCache = os.path.join(cacheFolder, tableId + ".property.star.cache")
        self.logger.debug("Identifying properties for a table %s"%(tableId))


        startTime = time.time()

        #load disambiguation from cache
        entities = []
        if os.path.exists(entitiesCacheFile):
            entities = pickle.load(open(entitiesCacheFile, 'rb'))
        else:
            raise EntitiesDataStructureNotFound("Entities data structure not available. Did you run subject column identification?")

        ## get all classes for those
        ## take the most frequent one
        ## filter out all other disambiguations
        ## annotate entities with classes
        if os.path.exists(entitiesWithClassesCache):
            entities = pickle.load(open(entitiesWithClassesCache, 'rb'))
        else:
            classSearchTimeStart = time.time()
            for rowIndex, entityRow in enumerate(entities):
                for columnIndex, entity in enumerate(entityRow):
                    for entityIndex, _entity in enumerate(entity):
                        entity[entityIndex] = (self.getClassForEntity(_entity), _entity)
            classSearchTimeEnd = time.time()
            self.classSearchTime = classSearchTimeEnd - classSearchTimeStart
            pickle.dump(entities, open(entitiesWithClassesCache, "wb" ) )

        classes = [[]]*numberOfColumns
        for rowIndex, entityRow in enumerate(entities):
            for columnIndex, entity in enumerate(entityRow):
                for entityIndex, _entity in enumerate(entity):
                    (_class, entityUrl) = _entity
                    try:
                        classes[columnIndex].append(_class)
                    except BaseException as e:
                        print "%s" % (str(e),)
        #identify the main class for the subject column
        classesSubjectColumn = [item for sublist in classes[subjectColumn] for item in sublist]
        try:
            classCount = len(classesSubjectColumn)
            (mainClass, mainClassCount) = Counter(classesSubjectColumn).most_common(1)[0]
            mainClassScore = float(mainClassCount) / classCount * 100
        except IndexError:
            self.logger.debug("Main class could not be identified")
            mainClass = ""

        #inject not mainClass row for a test
        #entities[0][subjectColumn][0] = (["gibberish:class"], "dbpedia:someCountry")

        #Wipe everything which is not mainClass
        #In subject column
        for rowIndex, entityRow in enumerate(entities):
            for columnIndex, entity in enumerate(entityRow):
                if columnIndex != subjectColumn:
                    continue
                for entityIndex, _entity in enumerate(entity):
                    (_class, entityUrl) = _entity
                    if not mainClass in _class:
                        entities[rowIndex][columnIndex][entityIndex] = (None, None)

        #find all properties for each entity-value pair
        properties = collections.defaultdict(dict)
        if os.path.exists(propertyCache):
            properties = pickle.load(open(propertyCache, 'rb'))
        else:
            propertySearchTimeStart = time.time()
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
                                try:
                                    cellValue = tableData[rowIndex][nonSubjectColumn]
                                    properties[rowIndex][nonSubjectColumn] = self.propertySearch.uriLiteralSearch(entityUrl,cellValue)
                                except:
                                    pass

            propertySearchTimeEnd = time.time()
            self.propertySearchTime = propertySearchTimeEnd - propertySearchTimeStart
            pickle.dump(properties, open(propertyCache, "wb" ) )

        #Aggregate properties for each atomic table
        propertiesAggregate = collections.defaultdict(dict)
        for nonSubjectColumn in nonSubjectColumns:
            propertiesAggregate[nonSubjectColumn] = []
        for row in properties:
            for nonSubjectColumn in nonSubjectColumns:
                try:
                    propertiesAggregate[nonSubjectColumn].append(properties[row][nonSubjectColumn])
                except:
                    pass

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

        #if subject column is identified then subject column should have rdfs:label property
        #topProperties.append(("http://www.w3.org/2000/01/rdf-schema#label", subjectColumn))

        endTime = time.time()
        self.executionTimeFull = endTime - startTime
        self.executionTimePure = self.executionTimeFull - self.disambiguationTime - self.classSearchTime - self.propertySearchTime

        #check if seed properties contain properties we are trying to find
        for _property in table.properties:
            if _property['uri'] in propertiesAggregate[_property['columnIndex']]:
                self.seedListContains += 1

        return topProperties
