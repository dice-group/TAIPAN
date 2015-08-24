import unittest

from taipan.Utils.Sampling import Sampler
from taipan.Relational.Parsers import MannheimParser
from taipan.Learning.SubjectColumnIdentification import SimpleIdentifier

class SimpleIdentifierTestCase(unittest.TestCase):
    def setUp(self):
        sampler = Sampler()
        randomTable = sampler.getRandomTables(1)[0]
        parser = MannheimParser(randomTable)
        self.simpleIdentifier = SimpleIdentifier(parser)

    def testSimpleColumnIdentification(self):
        colNumber = self.simpleIdentifier.identifySubjectColumn()
        self.assertIsInstance(colNumber, int, msg="colNumber should be of type int")
