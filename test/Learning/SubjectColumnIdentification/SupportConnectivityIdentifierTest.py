import unittest
import numpy

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification.SimpleIdentifier import SimpleIdentifier
from taipan.Learning.SubjectColumnIdentification.SupportConnectivityIdentifier import SupportConnectivityIdentifier

from taipan.Logging.Logger import Logger

class SupportConnectivityIdentifierTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.scIdentifier = SupportConnectivityIdentifier()
        self.testTables = sampler.getTablesSubjectIdentificationGoldStandard()
        #self.testTables = sampler.getTablesDbpediaWhitelistDataset()
        #self.testTables = sampler.getTablesDbpediaDataset()

    def testSupportConnectivityIdentifier(self):
        alphas = numpy.arange(0,1.1,0.1)
        for alpha in alphas:
            correctly = 0
            for table in self.testTables[:]:
                supportCeil = 100
                supportFloor = 0
                connectivityThreshold = 0
                subjectColumn = self.scIdentifier.identifySubjectColumn(table, supportFloor, supportCeil, connectivityThreshold, alpha)
                if table.isSubjectColumn(subjectColumn):
                    correctly += 1
            print "alpha: %s" %(alpha)
            print correctly
            print float(correctly) / len(self.testTables)
