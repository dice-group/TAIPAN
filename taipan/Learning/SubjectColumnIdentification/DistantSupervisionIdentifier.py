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
from taipan.Learning.EntityIdentification.AgdistisTableIdentifier import AgdistisTableIdentifier
import taipan.Config.Pathes
from taipan.Learning.SubjectColumnIdentification.SupportIdentifier import SupportIdentifier
from taipan.Search.PropertyTableSearch import PropertyTableSearch

class DistantSupervisionIdentifier(object):
    def __init__(self):
        self.logger = Logger().getLogger(__name__)
        self.agdistis = AgdistisTableIdentifier()
        self.supportIdentifier = SupportIdentifier()

    def identifySubjectColumn(self, table, rowsToAnalyze=20, rowsFromCache=None, support=0, connectivity=0, threshold=0):
        """
            rowsToAnalyze -- how many rows should be evaluated
            rowsFromCache -- can be used to reduce number of rows to be read from cache
            connectivity -- a number of relations subject column should have at least (absolute number)
            threshold -- percentage of subject columns identified inside the analyzed part of the table (divided by the total number of rows), i.e. 80% means that the same subject column identified for 80% of rows
        """
        tableData = table.getData()
        tableHeader = table.getHeader()
        tableId = table.id
        numberOfRows = len(tableData)
        numberOfColumns = len(tableData[0])

        self.logger.debug(tableId)

        self.executionStartTimePoint = 0
        self.executionEndTimePoint = 0
        self.executionTimeFull = 0
        self.executionTimePure = 0 #without querying and disambiguation
        self.queryTime = 0
        self.agdistisTime = 0

        self.executionStartTimePoint = time.time()
        #identify entities
        #TODO: get the score from agdistis
        agdistisStartTimePoint = time.time()
        entities = self.agdistis.disambiguateTable(table)
        agdistisEndTimePoint = time.time()
        self.agdistisTime = agdistisEndTimePoint - agdistisStartTimePoint

        #TODO: rename columnScores to supports
        columnScores = self.supportIdentifier.calculateSupport(entities)
        #Support based approach ends here: refactor into class
        relations = self.propertyTableSearch.findRelationsForTable(table, entities)

        #Make just a connectivity approach!!!


        #Calculate the connectivity for all the rows and then take average!
        #What we have a boolean classifier
        #Linear combination is better
        #Ten cross fold validation (or inverse)
        #just try different different weights a*connectivity + (1-a)*support --> equivalent for a*connectivity + b+support
        #For the combination -->

        import ipdb; ipdb.set_trace()

        subjectColumnScores = [0]*numberOfColumns
        for subjectColumn in subjectColumns:
            if subjectColumn != None:
                subjectColumnScores[subjectColumn] += 1

        #Normalize
        for columnIndex, subjectColumnScore in enumerate(subjectColumnScores):
            subjectColumnScores[columnIndex] = float(subjectColumnScore) / numberOfRows * 100

        import ipdb; ipdb.set_trace()
        #WRONG!!!!
        #subjectColumn = [columnIndex for columnIndex, columnScore in enumerate(subjectColumnScores) if columnScore >= threshold]

        self.executionEndTimePoint = time.time()
        self.executionTimeFull = self.executionEndTimePoint - self.executionStartTimePoint
        self.executionTimePure = self.executionTimeFull - self.queryTime - self.agdistisTime

        if(len(subjectColumn) <= 0):
            return None
        else:
            return subjectColumn[0]
