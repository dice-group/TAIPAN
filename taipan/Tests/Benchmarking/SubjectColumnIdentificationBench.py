import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification.SimpleIdentifier import SimpleIdentifier
from taipan.Learning.SubjectColumnIdentification.DistantSupervisionIdentifier import DistantSupervisionIdentifier

from taipan.Logging.Logger import Logger

class SimpleIdentifierBenchTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.simpleIdentifier = SimpleIdentifier()

    def testSimpleColumnIdentifierOne(self):
        colNumber = self.simpleIdentifier.identifySubjectColumn(self.testTable)
        self.assertTrue(self.testTable.isSubjectColumn(colNumber), msg="colNumber should be subject column")

class DistantSupervisionIdentifierBenchTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.dlIdentifier = DistantSupervisionIdentifier()
        #self.testTables20 = sampler.get20Tables()

    def testDistantLearningIdentifierOne(self):
        colNumber = self.dlIdentifier.identifySubjectColumn(self.testTable)
        self.assertTrue(self.testTable.isSubjectColumn(colNumber), msg="colNumber should be subject column")

    #def testDistantLearningIdentifierTwenty(self):
        # for table in self.testTables20:
        #     colNumber = self.dlIdentifier.identifySubjectColumn(table)
        #     print table.getHeader()
        #     print table.getData()[0]
        #     print table.classes
        #     print colNumber
        #     print ''
