import unittest
import logging

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.PropertyMapping.SimplePropertyMapper import SimplePropertyMapper

class SimplePropertyMappingTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTables = sampler.getTablesPropertyAnnotationDbpediaGoldStandard()
        self.propertyMapper = SimplePropertyMapper()

    def testMapProperties(self):
        logging.disable(logging.DEBUG)
        logging.disable(logging.INFO)
        for num, table in enumerate(self.testTables):
            propertyScores = self.propertyMapper.getScores(table)
            propertiesRetrieved = self.propertiesRetrievedByTP(propertyScores, table.propertiesGold)
            #(overall, correct) = self.diffProperties(properties, table.propertiesGold)
            print "%s, %s" % (propertiesRetrieved, len(table.propertiesGold),)

    def propertiesRetrievedByTP(self, propertyScores, propertiesGold):
        count = 0
        if propertyScores == []:
            return count
            
        for _property in propertiesGold:
            propertyScore = propertyScores[_property['columnIndex']].get(_property['uri'])
            if propertyScore != None:
                count += 1
        return count

    def diffProperties(self, propertiesMapped, propertiesGold):
        correct = 0
        overall = len(propertiesMapped)
        for propertyMapped in propertiesMapped:
            #find property with the same columnIndex
            for propertyGold in propertiesGold:
                if propertyMapped['columnIndex'] == propertyGold['columnIndex']:
                    if propertyMapped['uri'] == propertyGold['uri']:
                        correct += 1
        return (overall, correct)
