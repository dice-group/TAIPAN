import unittest

from taipan.Utils.Sampling import Sampler
from taipan.Relational.ParsersFactory import MannheimTables
from taipan.Learning.SubjectColumnIdentification import SimpleIdentifier

from taipan.Logging.Logger import Logger

class SimpleIdentifierTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger().getLogger(__name__)
        sampler = Sampler()
        randomTables = sampler.getRandomTables(10)
        self.tables = MannheimTables(randomTables).tables
        self.simpleIdentifier = SimpleIdentifier()

    def testBenchSimpleColumnIdentification(self):
        for table in self.tables:
            self.logger.info("Identifying subject column for table...")
            self.logger.info("%s" % (table.getTable(),))
            colNumber = self.simpleIdentifier.identifySubjectColumn(table)
            self.logger.info("Identified subject column %s" % (colNumber,))
