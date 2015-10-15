import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.PropertyMapping.SimpleCachePropertyMapper import SimpleCachePropertyMapper

class SimpleCachePropertyMappingTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.simplePropertyMapper = SimpleCachePropertyMapper()
        #self.testTables20 = sampler.get20Tables()
        #self.testTables = sampler.getTablesSubjectIdentification()

    def testMapProperties(self):
        properties = self.simplePropertyMapper.mapProperties(self.testTable)
        for _property in properties:
            (uri, index) = _property
            print "Property identified: %s" % (uri,)
            print "Column Index: %s" % (index,)
            print "Correct?"
            print self.testTable.isProperty(_property)
