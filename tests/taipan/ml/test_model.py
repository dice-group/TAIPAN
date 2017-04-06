"""Test for taipan.ml.subjectcolumn.model"""

from numpy import array

from taipan.ml.model import MLModel

MLMODEL = MLModel()

def test_get_tables():
    tables = MLMODEL.get_tables()
    assert len(tables) == 116

COLUMN = ['PORT' 'Australia' 'Bangladesh' 'Cambodia' 'Canada' 'France' 'Germany'
 'Hong Kong' 'India' 'Indonesia' 'Italy' 'Japan' 'Korea' 'Malaysia' 'Nepal'
 'New Zealand' 'Papua New Guinea' "People's Rep. of China" 'Philippines'
 'Portugal']
def test_calculate_feature_vector_column():
    table = MLMODEL.get_tables()[0]
    columns = table.table.transpose()
    col = columns[0]
    vec = MLMODEL.calculate_feature_vector_column(col, 0, table)
    assert vec == [0.15, 95.0, 1.0, 0.0, 0.0, 1.4]


def test_calculate_feature_vector():
    table = MLMODEL.get_tables()[0]
    (column_feature_vectors, target_vector) = MLMODEL.calculate_feature_vector(table)
    assert column_feature_vectors == [[0.15, 95.0, 1.0, 0.0, 0.0, 1.4], [0.13333333333333333, 75.0, 0.65, 0.0, 0.0, 1.0], [0.016666666666666666, 0.0, 0.75, 0.85, 0.0, 2.45]]
    assert target_vector == [True, False, False]


def test_calculate_feature_vectors():
    #TODO: next thang
    pass
