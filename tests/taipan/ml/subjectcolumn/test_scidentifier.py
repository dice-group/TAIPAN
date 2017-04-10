from taipan.ml.model import MLModel
from taipan.ml.subjectcolumn.scidentifier import SCIdentifier

SCIDENTIFIER = SCIdentifier()
MLMODEL = MLModel()

def test_get_model():
    model = SCIDENTIFIER.get_model()
    assert model.classes_.tolist() == [False, True]
    assert model.max_features_ == 6


def test_identify_subject_column():
    table = MLMODEL.get_tables()[0]
    subject_column = SCIDENTIFIER.identify_subject_column(table)
    assert subject_column == [0]
