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
        #self.testTables = sampler.getTablesSubjectIdentificationGoldStandard()
        self.testTables = sampler.getTablesDbpediaWhitelistDataset()

    def testSupportIdentifier(self):
        """
           support = 0 100 | 0.327868852459
           support = 0.8 97 | 0.327868852459
           support = 0.8 30 | 0.459016393443
           support = 0.8 40 | 0.409836065574
           support = 10 70 | 0.475409836066
        """
        correctly = 0
        for tableNum, table in enumerate(self.testTables):
            print "%s out of %s" % (tableNum, len(self.testTables))
            supportFloor = 10
            supportCeil = 70
            subjectColumn = self.scIdentifier.identifySubjectColumn(table, supportCeil, supportFloor)
            if table.isSubjectColumn(subjectColumn):
                correctly += 1

        macroAccuracy = float(correctly) / len(self.testTables)
        print correctly
        print len(self.testTables)
        print macroAccuracy
