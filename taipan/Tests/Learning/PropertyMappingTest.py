import unittest

from taipan.Utils.Sampling import Sampler
from taipan.Relational.Parsers import MannheimTable
from taipan.Learning.PropertyMapping import PropertyMapper

class PropertyMappingTestCase(unittest.TestCase):
    def setUp(self):
        sampler = Sampler()
        randomTable = sampler.getRandomTables(1)[0]
        self.table = MannheimTable(randomTable)
        self.propertyMapper = PropertyMapper()

    def testMapProperties(self):
        self.propertyMapper.mapProperties(self.table)
