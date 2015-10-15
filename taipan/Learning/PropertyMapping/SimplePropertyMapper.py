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

class SimplePropertyMapper(object):
    """
        This class do the property mapping for a given table
        Algorithm 2: Taipan Property Mapping Algorithm
    """

    def __init__(self):
        self.logger = Logger().getLogger(__name__)
        self.dlIdentifier = DistantSupervisionIdentifier()

    def mapProperties(self, table):
        tableData = table.getData()
        tableHeader = table.getHeader()
        tableId = table.id
        cacheFile = os.path.join(cacheFolder, tableId + ".relations.cache")
        subjectColumn = self.dlIdentifier.identifySubjectColumn(table)

        self.logger.debug("Identifying properties for a table %s"%(tableId))

        if(os.path.exists(cacheFile)):
            relations = pickle.load(open(cacheFile, 'rb'))
        else:
            raise RelationsDataStructureNotFound("Could not found Rels structure for %s"%(str(tableId),))

        self.executionTimeFull = 0
        self.startTime = time.time()
        #init properties
        nonSubjectColumns = range(0,len(relations[0]))
        nonSubjectColumns.remove(subjectColumn)
        properties = collections.defaultdict(dict)
        for nonSubjectColumn in nonSubjectColumns:
            properties[nonSubjectColumn] = []

        #Aggregate all properties
        for row in relations:
            for nonSubjectColumn in nonSubjectColumns:
                #This is properties for atomic table with h_i, i = nonSubjectColumn
                try:
                    properties[nonSubjectColumn].append(row[subjectColumn][nonSubjectColumn])
                except:
                    pass

        #Flatten the properties
        topProperties = []
        for nonSubjectColumn in nonSubjectColumns:
            properties[nonSubjectColumn] = [item for sublist in properties[nonSubjectColumn] for item in sublist]
            #and get the maximum
            try:
                topProperty = Counter(properties[nonSubjectColumn]).most_common(1)[0][0]
                topProperties.append((topProperty,nonSubjectColumn))
            except IndexError:
                self.logger.debug("No property identified for column %s"%(nonSubjectColumn))

        self.endTime = time.time()
        self.executionTimeFull = self.endTime - self.startTime
        return topProperties
