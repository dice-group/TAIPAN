import unittest

from taipan.Utils.Sampling import Sampler

class SamplingTestCase(unittest.TestCase):
    def testGetRandomTable(self):
        sampler = Sampler()
        table = sampler.getRandomTables(1)
        self.assertIsInstance(table, list, msg="Should return a list")
        self.assertEqual(len(table), 1, msg="Should return a list of length 1")
        self.assertIsInstance(table[0], str, msg="List should contain strings")
        self.assertGreater(len(table[0]), 0, msg="First element in the list (table) length should not be greater than 0")
