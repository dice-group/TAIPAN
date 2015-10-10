import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification.SimpleIdentifier import SimpleIdentifier

class SimpleIdentifierTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.simpleIdentifier = SimpleIdentifier()

    def testSimpleColumnIdentification(self):
        colNumber = self.simpleIdentifier.identifySubjectColumn(self.testTable)
        self.assertIsInstance(colNumber, int, msg="colNumber should be of type int")
