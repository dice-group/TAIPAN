from sklearn import tree
from taipan.util import loadCsv
from taipan.ml.model import MLModel

class SCIdentifier(object):
    def __init__(self):
        self.clf = tree.DecisionTreeClassifier(max_depth=5)
        self.mlmodel = MLModel()

    def fit(self):
        training_tables = self.mlmodel.get_tables()
        (featureVectors, targetVector) = self.calculateFeaturesTables(trainingTables)
        self.clf.fit(featureVectors, targetVector)


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
