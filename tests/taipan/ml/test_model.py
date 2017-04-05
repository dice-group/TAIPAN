"""Test for taipan.ml.subjectcolumn.model"""

from taipan.ml.model import MLModel

def test_get_tables():
    mlmodel = MLModel()
    tables = mlmodel.get_tables()
    assert len(tables) == 116

def test_calculate_feature_vector_column():
    mlmodel = MLModel()
    table = mlmodel.get_tables()[0]
    columns = table.table.transpose()
    col = columns[0]
    #vec = mlmodel.calculate_feature_vector_column(col, 0, table)
    #import ipdb; ipdb.set_trace()

def test_calculate_feature_vector():
    mlmodel = MLModel()
    table = mlmodel.get_tables()[0]
