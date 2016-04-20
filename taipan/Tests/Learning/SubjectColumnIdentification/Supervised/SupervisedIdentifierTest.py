import unittest
import numpy as np

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification.Supervised.SupervisedIdentifier import SupervisedIdentifier

from taipan.Logging.Logger import Logger

class SVMIdentifierTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.scIdentifier = SupervisedIdentifier(7, inverseCrossValidation=True, useColumnIndex=False)

    def testSupervisedIdentifier(self):
        """
            0 -- svm.SVC()
                recall: 0.466666666667
                false positives: 0.533333333333

            1 -- svm.LinearSVC(),
                recall: 0.2
                false positives: 0.8

            2 -- KNeighborsClassifier(),
                recall: 0.533333333333
                false positives: 0.6

            3 -- SGDClassifier(),
                recall: 0.733333333333
                false positives: 0.266666666667

            4 -- tree.DecisionTreeClassifier(),
                recall: 0.733333333333
                false positives: 0.266666666667

                max_depth=5
                recall: 0.8
                false positives: 0.2

            5 -- GradientBoostingClassifier()
                recall: 0.533333333333
                false positives: 0.466666666667

            6 -- NearestCentroid()
                recall: 0.416666666667
                false positives: 0.958333333333

            7 -- SGDClassifier(loss="perceptron", eta0=1, learning_rate="constant", penalty=None)
                recall: 0.333333333333
                false positives: 0.666666666667
        """
        testTables = self.scIdentifier.getTestingTables()
        annotatedTables = self.scIdentifier.getAnnotatedTables()
        recall = 0
        falsePositives = 0
        for table in testTables:
            subjectColumns = self.scIdentifier.identifySubjectColumn(table)
            if table.subjectColumn in subjectColumns:
                recall += 1
            elif len(subjectColumns) > 0:
                falsePositives += len(subjectColumns)
        tableGuessedCorrectly = recall
        recall = float(recall) / len(testTables)
        precision_1 = float(falsePositives) / len(testTables)
        fmeasure = recall*precision_1
        print "table guessed: %s" % len(testTables)
        print "table guessed correctly: %s" % tableGuessedCorrectly
        print "table used for learning: %s" % len(annotatedTables)
