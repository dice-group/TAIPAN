import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification.SimpleIdentifier import SimpleIdentifier
from taipan.Learning.SubjectColumnIdentification.SupportIdentifier import SupportIdentifier

from taipan.Logging.Logger import Logger

class SupportIdentifierTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.scIdentifier = SupportIdentifier()
        self.testTables = sampler.getTablesSubjectIdentification()

    def testSupportIdentifier(self):
        for table in self.testTables:
            print table.table
            support = 0
            subjectColumn = self.scIdentifier.identifySubjectColumn(table, support=support)
            import ipdb; ipdb.set_trace()
            print "subjectColumn %s" % (table.subjectColumn,)
            print "identified %s" % (subjectColumn,)
            print table.table[0:5]
