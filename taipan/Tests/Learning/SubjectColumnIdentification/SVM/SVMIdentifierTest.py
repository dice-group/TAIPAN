import unittest
import numpy as np

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification.SimpleIdentifier import SimpleIdentifier
from taipan.Learning.SubjectColumnIdentification.ConnectivityIdentifier import ConnectivityIdentifier

from taipan.Logging.Logger import Logger

class SVMIdentifierTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.scIdentifier = ConnectivityIdentifier()
        self.testTables = sampler.getTablesSubjectIdentification()

    def testSVMIdentifier(self):
        """
        """
        pass

    def calculateFeatures(self):
        columns = {"data": np.ndarray([]), "target": np.ndarray([])}
        features = []
        target = []
        for table in self.testTables:
            (columnFeatureVectors, targetVector) = self.calculateFeaturesTable(table)
            features.extend(columnFeatureVectors)
            target.extend(targetVector)

        return (features, target)

    def nFoldValidation(self, fold):
        (data, target) = self.calculateFeatures()
        trainingData = data[:len(data)/fold]
        trainingTarget = target[:len(target)/fold]
        validationData = data[len(data)/fold:]
        validationTarget = target[len(target)/fold:]

        self.clf.fit(trainingData, trainingTarget)

        predictedValues = self.clf.predict(validationData)
        count = 0
        falsePositives = 0
        falseNegatives = 0
        for idx, predictedValue in enumerate(predictedValues):
            if predictedValue == validationTarget[idx]:
                count += 1
            elif predictedValue == True:
                falsePositives += 1
            elif predictedValue == False:
                falseNegatives += 1

        precision = float(count) / len(validationTarget)
        print "precision: %s" % (precision,)
        print "false positives: %s" % (falsePositives,)
        print "false negatives: %s" % (falseNegatives,)
