import os

from sklearn import tree
from sklearn.externals import joblib

from taipan.util import load_csv
from taipan.ml.model import MLModel
from taipan.pathes import SCI_MODEL


class SCIdentifier(object):
    def __init__(self):
        self.clf = self.get_model()

    def get_model(self):
        clf = None
        if os.path.exists(SCI_MODEL):
            clf = joblib.load(SCI_MODEL)
        else:
            mlmodel = MLModel()
            training_tables = mlmodel.get_tables()
            (feature_vectors, target_vector) = mlmodel.calculate_feature_vectors(training_tables)
            clf = tree.DecisionTreeClassifier(max_depth=5)
            clf.fit(feature_vectors, target_vector)
            joblib.dump(clf, SCI_MODEL)
        return clf

    def identify_subject_column(self, table):
        subject_column = []
        mlmodel = MLModel()
        (feature_vector, target_vector) = mlmodel.calculate_feature_vector(table)
        for col_i, is_sc in enumerate(self.clf.predict(feature_vector).tolist()):
            if is_sc:
                subject_column.append(col_i)
        return subject_column
