import os

from taipan.pathes import SUBJECT_COLUMN_LIST
from taipan.util import load_csv
from taipan.ml.table import Table

from taipan.ml.subjectcolumn.features import Connectivity, Support, \
         CellsWithUniqueContentFraction, CellsWithNumericContentFraction, \
         VarianceInDateTokens, NumberOfWordsAverage

ROWS_TO_ANALYZE = os.environ.get("ROWS_TO_ANALYZE", "20")
FEATURE_LIST = [Connectivity(), Support(), CellsWithUniqueContentFraction(), CellsWithNumericContentFraction(), VarianceInDateTokens(), NumberOfWordsAverage()]

class MLModel(object):
    def get_tables(self):
        tables = []

        id_list = load_csv(SUBJECT_COLUMN_LIST)
        id_list = map((lambda x: x[0]), id_list)

        for _id in id_list:
            table = Table(_id)
            table.init()
            table.table = table.table[:int(ROWS_TO_ANALYZE)]
            tables.append(table)
        return tables

    def calculate_feature_vectors(self, tables):
        feature_vectors = []
        target_vectors = []
        for table in tables:
            (feature_vector, target_vector) = self.calculate_feature_vector(table)
            feature_vectors.extend(feature_vector)
            target_vectors.extend(target_vector)
        return (feature_vectors, target_vectors)

    def calculate_feature_vector(self, table):
        columns = table.table.transpose()
        column_feature_vectors = []
        target_vector = []
        for col_i, col in enumerate(columns):
            feature_vector = self.calculate_feature_vector_column(col, col_i, table)
            column_feature_vectors.append(feature_vector)
            target_vector.append(table.is_subject_column(col_i))
        return (column_feature_vectors, target_vector)

    def calculate_feature_vector_column(self, col, col_i, table):
        feature_vector = []
        for feature in FEATURE_LIST:
            feature_vector.append(feature.calculate(col, col_i, table))
        return feature_vector
