import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.PropertyRecommendation.SimplePropertyRecommender import SimplePropertyRecommender

class SimplePropertyRecommenderTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTables = sampler.getTablesPropertyAnnotation()
        self.spr = SimplePropertyRecommender()

    def testRecommendPropertiesForTable(self):
        for num, table in enumerate(self.testTables):
            print "table %s" %(num,)
            properties = self.spr.recommendPropertiesForTable(table)
            import ipdb; ipdb.set_trace()

    def testLookupPropertiesLOV(self):
        columnHeader = "city"
        properties = self.spr.lookupPropertiesLOV(columnHeader)
