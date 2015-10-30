from sklearn import svm
import numpy as np

from taipan.T2D.Sampler import T2DSampler
from taipan.Learning.SubjectColumnIdentification.SVM.Features import FeatureList

class SVMIdentifier(object):
    """
        According to Recovering Semantics of Tables on The Web, 2011
        should have precision of 94%
        Features to use:
        - Fraction of cells with unique content
        - Fraction of cells with numeric content
        - Average number of letters in each cell
        - Average number of numbers in each cell
        - Average number of words in each cell
        - Column index from left
    """
    fold=10
    def __init__(self):
        self.clf = svm.SVC(gamma=0.001, C=100.)
        (featureVectors, targetVector) = self.calculateFeaturesTables()
        self.trainingFeatureVectors = featureVectors[:fold-1]
        self.trainingTargetVector = targetVector[:fold-1]
        self.validationFeatureVectors = featureVectors[fold-1:]
        self.validationTargetVector = targetVector[fold-1:]
        self.clf.fit(self.trainingFeatureVectors, self.trainingTargetVector)

    def calculateFeaturesColumn(self, column, columnIndex):
        featureVector = []
        for feature in FeatureList:
            featureVector.append(feature.calculate(column))
        return featureVector

    def calculateFeaturesTable(self, table):
        tableData = table.getData()
        tableColumns = tableData.transpose()
        columnFeatureVectors = []
        targetVector = []
        for columnIndex, column in enumerate(tableColumns):
            columnFeatureVectors.append(self.calculateFeaturesColumn(column, columnIndex))
            targetVector.append(table.isSubjectColumn(columnIndex))
        return (columnFeatureVectors, targetVector)

    def calculateFeaturesTables(self, annotatedTables):
        featureVectors = []
        targetVector = []
        for table in annotatedTables:
            (tableFeatureVector, tableTargetVector) = self.calculateFeaturesTable(table)
            featureVectors.extend(columnFeatureVectors)
            targetVector.extend(tableTargetVector)
        return (featureVectors, targetVector)

    def getAnnotatedTables(self):
        sampler = T2DSampler()
        tables = sampler.getTablesSubjectIdentification()[:self.fold]

    def getTestingTables(self):
        sampler = T2DSampler()
        return sampler.getTablesSubjectIdentification()[self.fold:]

    def identifySubjectColumn(self, table):
        predictedValues = self.clf.predict(validationData)

if __name__ == "__main__":
    import ipdb; ipdb.set_trace()
    svm = SVMIdentifier()
    svm.nFoldValidation(3)
