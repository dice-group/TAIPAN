import unittest
import numpy as np

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification.SimpleIdentifier import SimpleIdentifier

from taipan.Logging.Logger import Logger

class SVMIdentifierTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTables = sampler.getTablesSubjectIdentificationGoldStandard()
        self.scIdentifier = SimpleIdentifier()

    def testSimpleIdentifier(self):
        recall = 0
        falsePositives = 0
        tableGuessedCorrectly = 0
        for table in self.testTables:
            subjectColumn = self.scIdentifier.identifySubjectColumn(table)
            if table.subjectColumn == subjectColumn:
                tableGuessedCorrectly += 1
        print "table guessed: %s" % len(self.testTables)
        print "table guessed correctly: %s" % tableGuessedCorrectly

    def testSimpleIdentifierPermutations(self):
        recall = 0
        falsePositives = 0
        tableGuessedCorrectly = 0
        for table in self.testTables:
            table.scrumbleColumns()
            subjectColumn = self.scIdentifier.identifySubjectColumn(table)
            if table.subjectColumn == subjectColumn:
                tableGuessedCorrectly += 1
        print "Permutations result"
        print "table guessed: %s" % len(self.testTables)
        print "table guessed correctly: %s" % tableGuessedCorrectly
