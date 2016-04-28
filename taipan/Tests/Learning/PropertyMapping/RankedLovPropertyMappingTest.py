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
        self.testTables = sampler.getTablesDbpediaWhitelistDataset()

    def testMapProperties(self):
        logging.disable(logging.DEBUG)
        logging.disable(logging.INFO)
        pp = pprint.PrettyPrinter(indent=4)
        for i in [0.8]:
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
                print "%s" %(table.id)
                print "Overall: %s" % (overall,)
                pp.pprint(allproperties)
                print "Correct: %s" % (correct,)
                pp.pprint(table.propertiesGold)

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

        mapped = False
        for propertyMapped in propertiesMapped:
            if propertyMapped['columnIndex'] == subjectColumn:
                correct += 1
                mapped = True

        if(not mapped):
            correct += 1
            overall += 1

        for propertyMapped in propertiesMapped:
            #find property with the same columnIndex
            for propertyGold in propertiesGold:
                if propertyMapped['columnIndex'] == propertyGold['columnIndex']:
                    if propertyMapped['uri'] == propertyGold['uri']:
                        correct += 1
        return (overall, correct)
