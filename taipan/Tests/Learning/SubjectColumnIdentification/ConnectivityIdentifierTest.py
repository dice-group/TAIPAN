import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification.SimpleIdentifier import SimpleIdentifier
from taipan.Learning.SubjectColumnIdentification.ConnectivityIdentifier import ConnectivityIdentifier

from taipan.Logging.Logger import Logger

class SupportIdentifierTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.scIdentifier = ConnectivityIdentifier()
        self.testTables = sampler.getTablesSubjectIdentification()

    def testSupportIdentifier(self):
        """
            not weighted 0.508196721311
            weighted 0.393442622951
        """
        precision = 0
        for table in self.testTables:
            print table.table
            subjectColumn = self.scIdentifier.identifySubjectColumn(table, applyWeights=True)
            if table.isSubjectColumn(subjectColumn):
                precision += 1
        print float(precision) / len(self.testTables)
