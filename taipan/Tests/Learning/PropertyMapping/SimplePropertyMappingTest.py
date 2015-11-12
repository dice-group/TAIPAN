import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.PropertyMapping.SimplePropertyMapper import SimplePropertyMapper

class SimplePropertyMappingTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTables = sampler.getTablesSubjectIdentification()
        self.simplePropertyMapper = SimplePropertyMapper()

    def testMapProperties(self):
        import logging
        logger = logging.getLogger("taipan.Learning.PropertyMapping.SimplePropertyMapper")
        logger.disabled = True

        for num, table in enumerate(self.testTables):
            print "table %s" %(num,)
            properties = self.simplePropertyMapper.mapProperties(table)
            toPrint = ""
            for _property in properties:
                (uri, index) = _property
                toPrint += "Uri: %s Column Index %s \n" % (uri,index)
            print toPrint
            print table.properties
            print table.table[:5]
