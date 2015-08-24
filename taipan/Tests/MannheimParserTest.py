import unittest
import numpy

from taipan.Utils.Sampling import Sampler
from taipan.Relational.Parsers import MannheimParser

class MannheimParserTestCase(unittest.TestCase):
    def setUp(self):
        sampler = Sampler()
        randomTable = sampler.getRandomTables(1)[0]
        self.parser = MannheimParser(randomTable)

    def testTableExist(self):
        table = self.parser.getTable()
        self.assertIsInstance(table, numpy.ndarray, msg="getTable() should return numpy.ndarray")
        self.assertGreater(len(table), 0, msg="getTable() should return non empty table")
