import unittest
import numpy as np

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification.SVM.SVMIdentifier import SVMIdentifier

from taipan.Logging.Logger import Logger

class SVMIdentifierTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.scIdentifier = SVMIdentifier()
        #self.testTables = sampler.getTablesSubjectIdentification()

    def testSVMIdentifier(self):
        testTables = self.scIdentifier.getTestingTables()
        recall = 0
        falsePositives = 0
        for table in testTables:
            subjectColumns = self.scIdentifier.identifySubjectColumn(table)
            if table.subjectColumn in subjectColumns:
                recall += 1
            elif len(subjectColumns) > 0:
                falsePositives += len(subjectColumns)
        recall = float(recall) / len(testTables)
        precision_1 = float(falsePositives) / len(testTables)
        fmeasure = recall*precision_1
        print "recall: %s" % recall
        print "false positives: %s" % precision_1
        #print "f measure: %s" % fmeasure
