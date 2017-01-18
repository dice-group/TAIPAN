import unittest
import logging
import numpy
import pprint

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.PropertyMapping.RankedLovPropertyMapper import RankedLovPropertyMapper

class RankedLovPropertyMappingTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        #self.testTables = sampler.getTablesPropertyAnnotationDbpediaGoldStandard()
        #self.propertyMapper = RankedLovPropertyMapper(scoreThreshold=0.8)
        #self.testTables = sampler.getTablesSyntheticDbpediaDataset()
        #self.testTables = sampler.getTablesDbpediaWhitelistDataset()
        self.testTables = sampler.getTablesDbpediaDataset()

    def testMapProperties(self):
        logging.disable(logging.DEBUG)
        logging.disable(logging.INFO)
        pp = pprint.PrettyPrinter(indent=4)
        for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
            propertyMapper = RankedLovPropertyMapper(scoreThreshold=i)
            retrieved = 0
            correctly = 0
            propertiesGold = 0
            for num, table in enumerate(self.testTables):
                (properties, allproperties) = propertyMapper.mapProperties(table)

                (overall, correct) = self.diffProperties(properties, table.propertiesGold, table.subjectColumn)
                retrieved += overall
                correctly += correct
                propertiesGold += len(table.propertiesGold)
                # print "%s" %(table.id)
                # print "Overall: %s" % (overall,)
                # pp.pprint(allproperties)
                # print "Correct: %s" % (correct,)
                # pp.pprint(table.propertiesGold)

            precision = float(correctly) / retrieved
            recall = float(correctly) / propertiesGold
            fmeasure = 2*(recall*precision)/(recall+precision)
            print "threshold: %s"%(i,)
            print "precision: %s"%(precision,)
            print "recall: %s"%(recall,)
            print "fmeasure: %s"%(fmeasure,)

    def diffProperties(self, propertiesMapped, propertiesGold, subjectColumn):
        correct = 0
        overall = len(propertiesMapped)

        for propertyMapped in propertiesMapped:
            #find property with the same columnIndex
            for propertyGold in propertiesGold:
                if propertyMapped['columnIndex'] == propertyGold['columnIndex']:
                    if propertyMapped['uri'] == propertyGold['uri']:
                        correct += 1
        return (overall, correct)
