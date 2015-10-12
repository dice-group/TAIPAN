import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable

class SamplerTest(unittest.TestCase):
    def setUp(self):
        self.sampler = T2DSampler()

    def testGetTablesForSubjectIdentification(self):
        tableForSubjectIdentification = self.sampler.getTablesSubjectIdentification()
        import ipdb; ipdb.set_trace
        #colNumber = self.simpleIdentifier.identifySubjectColumn(self.testTable)
        #self.assertIsInstance(colNumber, int, msg="colNumber should be of type int")
