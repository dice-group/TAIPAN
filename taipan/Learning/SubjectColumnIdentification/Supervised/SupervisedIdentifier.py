from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn import tree
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

import numpy as np

from taipan.T2D.Sampler import T2DSampler
from taipan.Learning.SubjectColumnIdentification.Supervised.Features import FeatureList

class SupervisedIdentifier(object):
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
    fold = 10
    inverseCrossValidation = False
    useColumnIndex = False
    selectKBest = SelectKBest(chi2, k="all")

    classifiers = [
        svm.SVC(),
        svm.LinearSVC(),
        KNeighborsClassifier(),
        SGDClassifier(loss="hinge", penalty="l2"),
        tree.DecisionTreeClassifier(max_depth=5),
        GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0),
        NearestCentroid(),
        SGDClassifier(loss="perceptron", eta0=1, learning_rate="constant", penalty=None)
    ]

    def __init__(self, classifierType=4, inverseCrossValidation=False, useColumnIndex=False):
        self.inverseCrossValidation = inverseCrossValidation
        self.useColumnIndex = useColumnIndex
        self.clf = self.classifiers[classifierType]
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
            featureVector = self.calculateFeaturesColumn(column, columnIndex, table)
            if self.useColumnIndex:
                featureVector.append(columnIndex)
            columnFeatureVectors.append(featureVector)
            targetVector.append(table.isSubjectColumn(columnIndex))
        return (columnFeatureVectors, targetVector)

    def calculateFeaturesTables(self, annotatedTables):
        featureVectors = []
        targetVector = []
        for table in annotatedTables:
            (tableFeatureVector, tableTargetVector) = self.calculateFeaturesTable(table)
            featureVectors.extend(tableFeatureVector)
            targetVector.extend(tableTargetVector)

        #get k best features
        self.selectKBest.fit(featureVectors, targetVector)

        return (self.selectKBest.transform(featureVectors), targetVector)

    def getTables(self):
        sampler = T2DSampler()
        return sampler.getTablesSubjectIdentificationGoldStandard()

    def getAnnotatedTables(self):
        fold = self.fold
        tables = self.getTables()
        if fold == None:
            return tables
        if not self.inverseCrossValidation:
            length = int(len(tables)/fold*(fold-1))
            return tables[:length]
        else:
            length = int(len(tables)/fold)
            return tables[:length]

    def getTestingTables(self):
        fold = self.fold
        tables = self.getTables()
        if fold == None:
            return []

        if not self.inverseCrossValidation:
            length = int(len(tables)/fold*(fold-1))
            return tables[length:]
        else:
            length = int(len(tables)/fold)
            return tables[length:]

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
        tableFeatureVector = self.selectKBest.transform(tableFeatureVector)
        predictedValues = self.clf.predict(tableFeatureVector).tolist()
        subjectColumnIndices = self.getIndicesValue(predictedValues, True)
        if subjectColumnIndices == []:
            return [-1]
        else:
            return subjectColumnIndices
