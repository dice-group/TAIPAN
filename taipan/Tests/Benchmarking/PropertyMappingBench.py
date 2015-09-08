import unittest

from taipan.Utils.Sampling import Sampler
from taipan.Relational.ParsersFactory import MannheimTables
from taipan.Learning.PropertyMapping import PropertyMapper

from taipan.Logging.Logger import Logger

class PropertyMappingBenchTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger().getLogger(__name__)
        sampler = Sampler()
        randomTables = sampler.getRandomTables(10)
        self.tables = MannheimTables(randomTables).tables
        self.propertyMapper = PropertyMapper()

    def testMapProperties(self):
        for table in self.tables:
            self.logger.info("Mapping properties for table...")
            self.logger.info("%s" % (table.getTable(),))
            properties = self.propertyMapper.mapProperties(table)
            self.logger.info("Identified subject column %s" % (colNumber,))
