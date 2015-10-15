import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.PropertyMapping.SimplePropertyMapper import SimplePropertyMapper

class PropertyMappingTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.simplePropertyMapper = SimplePropertyMapper()
        #self.testTables20 = sampler.get20Tables()
        #self.testTables = sampler.getTablesSubjectIdentification()

    def testMapProperties(self):
        self.simplePropertyMapper.mapProperties(self.testTable)
