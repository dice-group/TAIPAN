import unittest
import logging

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.PropertyMapping.LovPropertyMapper import LovPropertyMapper

class LovPropertyMappingTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTables = sampler.getTablesPropertyAnnotationDbpediaGoldStandard()
        self.propertyMapper = LovPropertyMapper(scoreThreshold=1.0)

    def testMapProperties(self):
        logging.disable(logging.DEBUG)
        logging.disable(logging.INFO)
        for num, table in enumerate(self.testTables):
            properties = self.propertyMapper.mapProperties(table)
            (overall, correct) = self.diffProperties(properties, table.propertiesGold)
            print "%s, %s" % (overall, correct,)

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
