import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.PropertyMapping.SimplePropertyMapper import SimplePropertyMapper

from taipan.Logging.Logger import Logger

class SimpleCachePropertyMappingBenchTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.logger = Logger().getLogger(__name__)
        self.simplePropertyMapper = SimplePropertyMapper()
        self.testTable = sampler.getTestTable()
        #self.testTables20 = sampler.get20Tables()
        #self.testTables = sampler.getTablesSubjectIdentification()

    def determineResultsFilename(self, filename):
        import os
        while os.path.exists(os.path.join("results",filename)):
            filename = filename.split(".")
            index = str(int(filename.pop()) + 1)
            filename.append(index)
            filename = ".".join(filename)

        filename = os.path.join("results",filename)
        return filename

    def resultsIterativePrinter(self, row, filename):
        import csv
        with open(filename, 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(row)


    def simplePropertyMapping(self, tables, rowsToDisambiguate=20, threshold=10):
        resultsFilename = "%srows.%sthreshold.propertyMapping.results.csv.1" %(rowsToDisambiguate, threshold)
        resultsFilename = self.determineResultsFilename(resultsFilename)
        header = ["tableId","propertyIdentified","correctly","falsePositives","notIdentified","seedListContains","executionTimeFull","executionTimePure","disambiguationTime","classSearchTime","propertySearchTime"]
        self.resultsIterativePrinter(header,resultsFilename)

        for table in tables:
            properties = self.simplePropertyMapper.mapProperties(table,rowsToDisambiguate, threshold)
            executionTimeFull = self.simplePropertyMapper.executionTimeFull
            executionTimePure = self.simplePropertyMapper.executionTimePure
            disambiguationTime = self.simplePropertyMapper.disambiguationTime
            classSearchTime = self.simplePropertyMapper.classSearchTime
            propertySearchTime = self.simplePropertyMapper.propertySearchTime
            seedListContains = self.simplePropertyMapper.seedListContains
            falsePositives = 0
            falseNegatives = table.getNumberOfProperties()
            correct = 0
            propertiesString = u""
            lastItem = len(properties) - 1
            for i, _property in enumerate(properties):
                (uri, index) = _property
                if table.isProperty(_property):
                    correct += 1
                    falseNegatives -= 1
                else:
                    falsePositives += 1
                if i == lastItem:
                    propertiesString += uri
                else:
                    propertiesString += uri + u"|"

            result = [table.id, propertiesString, correct, falsePositives,falseNegatives,seedListContains,executionTimeFull,executionTimePure,disambiguationTime,classSearchTime,propertySearchTime]
            self.resultsIterativePrinter(result,resultsFilename)

    def testMapProperties(self):
        tables = [self.testTable]
        #tables = self.testTables
        self.simplePropertyMapping(tables)
