import unittest
import logging

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.PropertyMapping.RankedLovPropertyMapper import RankedLovPropertyMapper

class RankedLovPropertyMappingTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        #self.testTables = sampler.getTablesPropertyAnnotationDbpediaGoldStandard()
        self.testTables = sampler.getTablesSyntheticDbpediaDataset()
        self.propertyMapper = RankedLovPropertyMapper(scoreThreshold=0.8)

    def testMapProperties(self):
        logging.disable(logging.DEBUG)
        logging.disable(logging.INFO)
        retrieved = 0
        correctly = 0
        propertiesGold = 0
        for num, table in enumerate(self.testTables):
            properties = self.propertyMapper.mapProperties(table)
            (overall, correct) = self.diffProperties(properties, table.propertiesGold)
            retrieved += overall
            correctly += correct
            propertiesGold += len(table.propertiesGold)

        precision = float(correctly) / retrieved
        recall = float(correctly) / propertiesGold
        fmeasure = 2*(recall*precision)/(recall+precision)
        print "precision: %s"%(precision,)
        print "recall: %s"%(recall,)
        print "fmeasure: %s"%(fmeasure,)

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
