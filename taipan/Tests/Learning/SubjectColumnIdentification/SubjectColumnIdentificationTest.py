import unittest

from taipan.Utils.Sampling import Sampler
from taipan.Relational.Parsers import MannheimTable
from taipan.Learning.SubjectColumnIdentification import SimpleIdentifier

class SimpleIdentifierTestCase(unittest.TestCase):
    def setUp(self):
        sampler = Sampler()
        randomTable = sampler.getRandomTables(1)[0]
        self.table = MannheimTable(randomTable)
        self.simpleIdentifier = SimpleIdentifier()

    def testSimpleColumnIdentification(self):
        colNumber = self.simpleIdentifier.identifySubjectColumn(self.table)
        self.assertIsInstance(colNumber, int, msg="colNumber should be of type int")
