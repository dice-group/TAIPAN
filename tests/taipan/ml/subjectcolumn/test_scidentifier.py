from taipan.ml.model import MLModel
from taipan.ml.subjectcolumn.scidentifier import SCIdentifier
from taipan.generictable import GenericTable

SCIDENTIFIER = SCIdentifier()
MLMODEL = MLModel()

def test_get_model():
    model = SCIDENTIFIER.get_model()
    assert model.classes_.tolist() == [False, True]
    assert model.max_features_ == 6


def test_identify_subject_column():
    table = MLMODEL.get_tables()[0]
    subject_column = SCIDENTIFIER.identify_subject_column(table)
    assert isinstance(subject_column, list)
    assert len(subject_column) > 0


def test_identify_subject_column_table_string():
    table_string = "\"Region\",\"Currency\",\"Price\",\"Price in ?\"\n\"Australia SA+WA\",\"AUD\",\"24.95\",\"15.91\"\n\"Israel\",\"ILS\",\"79\",\"15.03\"\n\"Australia\",\"AUD\",\"19.99\",\"12.75\"\n\"Kuwait\",\"KWD\",\"4.50\",\"11.08\"\n\"Canada\",\"CAD\",\"14.99\",\"10.02\""
    table = GenericTable("stub", csv_string=table_string)
    table.init()
    sc = SCIDENTIFIER.identify_subject_column(table)
    # table can not be predicted, [0] is returned by default
    assert isinstance(sc, list)
    assert len(sc) > 0
