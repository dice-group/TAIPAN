import unittest
import numpy

from taipan.Utils.Sampling import Sampler
from taipan.Relational.Parsers import MannheimTable

class MannheimTableTestCase(unittest.TestCase):
    def setUp(self):
        sampler = Sampler()
        randomTable = sampler.getRandomTables(1)[0]
        self.parser = MannheimTable(randomTable)

    def testTableExist(self):
        table = self.parser.getTable()
        self.assertIsInstance(table, numpy.ndarray, msg="getTable() should return numpy.ndarray")
        self.assertGreater(len(table), 0, msg="getTable() should return non empty table")
