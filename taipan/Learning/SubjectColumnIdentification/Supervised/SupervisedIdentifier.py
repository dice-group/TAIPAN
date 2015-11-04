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
    #set to None for production
    fold=10

    def __init__(self):
        self.clf = svm.SVC()
        #self.clf = svm.LinearSVC()
        trainingTables = self.getAnnotatedTables()
        (featureVectors, targetVector) = self.calculateFeaturesTables(trainingTables)
        self.clf.fit(featureVectors, targetVector)

    def calculateFeaturesColumn(self, column, columnIndex, table):
        featureVector = []
        for feature in FeatureList:
            featureVector.append(feature.calculate(column, columnIndex, table))
        return featureVector

    def calculateFeaturesTable(self, table):
        tableData = table.getData()
        tableColumns = tableData.transpose()
        columnFeatureVectors = []
        targetVector = []
        for columnIndex, column in enumerate(tableColumns):
            columnFeatureVectors.append(self.calculateFeaturesColumn(column, columnIndex, table))
            targetVector.append(table.isSubjectColumn(columnIndex))
        return (columnFeatureVectors, targetVector)

    def calculateFeaturesTables(self, annotatedTables):
        featureVectors = []
        targetVector = []
        for table in annotatedTables:
            (tableFeatureVector, tableTargetVector) = self.calculateFeaturesTable(table)
            featureVectors.extend(tableFeatureVector)
            targetVector.extend(tableTargetVector)
        return (featureVectors, targetVector)

    def getTables(self):
        sampler = T2DSampler()
        return sampler.getTablesSubjectIdentification()

    def getAnnotatedTables(self):
        fold = self.fold
        tables = self.getTables()
        if fold != None:
            length = int(len(tables)/fold*(fold-1))
            return tables[:length]
        else:
            return tables

    def getTestingTables(self):
        fold = self.fold
        tables = self.getTables()
        if fold != None:
            length = int(len(tables)/fold*(fold-1))
            return tables[length:]
        else:
            return []

    def getIndicesValue(self, lst, value):
        start_at = -1
        locs = []
        while True:
            try:
                loc = lst.index(value,start_at+1)
            except ValueError:
                break
            else:
                locs.append(loc)
                start_at = loc
        return locs

    def identifySubjectColumn(self, table):
        (tableFeatureVector, tableTargetVector) = self.calculateFeaturesTable(table)
        predictedValues = self.clf.predict(tableFeatureVector).tolist()
        subjectColumnIndices = self.getIndicesValue(predictedValues, True)
        if subjectColumnIndices == []:
            return [-1]
        else:
            return subjectColumnIndices
