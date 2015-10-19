import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification.SimpleIdentifier import SimpleIdentifier
from taipan.Learning.SubjectColumnIdentification.DistantSupervisionIdentifier import DistantSupervisionIdentifier

from taipan.Logging.Logger import Logger

# class SimpleIdentifierBenchTestCase(unittest.TestCase):
#     def setUp(self):
#         sampler = T2DSampler()
#         self.testTable = sampler.getTestTable()
#         self.simpleIdentifier = SimpleIdentifier()

    # def testSimpleColumnIdentifierOne(self):
    #     colNumber = self.simpleIdentifier.identifySubjectColumn(self.testTable)
    #     self.assertTrue(self.testTable.isSubjectColumn(colNumber), msg="colNumber should be subject column")

class SubjectColumnIdentificationBenchTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.dlIdentifier = DistantSupervisionIdentifier()
        self.simpleIdentifier = SimpleIdentifier()
        #self.testTables20 = sampler.get20Tables()
        #self.testTables = sampler.getTablesSubjectIdentification()

    def testDistantLearningIdentifierOne(self):
        colNumber = self.dlIdentifier.identifySubjectColumn(self.testTable)
        print "Identified subject column: %s" % (colNumber,)
        print "Correct? %s" % (self.testTable.isSubjectColumn(colNumber),)
