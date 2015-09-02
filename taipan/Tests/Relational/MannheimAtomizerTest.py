import unittest
import numpy

from taipan.Utils.Sampling import Sampler
from taipan.Relational.Parsers import MannheimTable
from taipan.Relational.Atomizers import MannheimAtomizer

class MannheimAtomizerTestCase(unittest.TestCase):
    def setUp(self):
        sampler = Sampler()
        randomTable = sampler.getRandomTables(1)[0]
        self.table = MannheimTable(randomTable)
        self.mannheimAtomizer = MannheimAtomizer()

    def testAtomizeTable(self):
        atomicTables = self.mannheimAtomizer.atomizeTable(self.table)
        self.assertTrue(len(atomicTables) > 0, msg="atomicTables should be a list with length > 0")
        self.assertTrue(len(atomicTables[0]) > 0, msg="first atomic table should be not empty, i.e. longer than 0")
        self.assertTrue(len(atomicTables[0]) == 2, msg="atomic table should be of length 2")
