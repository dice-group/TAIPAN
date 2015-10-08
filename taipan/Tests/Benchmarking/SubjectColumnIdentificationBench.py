import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification import SimpleIdentifier

from taipan.Logging.Logger import Logger

class SimpleIdentifierBenchTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.simpleIdentifier = SimpleIdentifier()

    def testSimpleColumnIdentificationOne(self):
        colNumber = self.simpleIdentifier.identifySubjectColumn(self.testTable)
        self.assertTrue(self.testTable.isSubjectColumn(colNumber), msg="colNumber should be subject column")
