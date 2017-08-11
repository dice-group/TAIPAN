"""Tests for taipan.entitysearch"""

from taipan.entitysearch.taipanentitysearch import disambiguate_subject_column
from taipan.ml.model import MLModel

def test_disambiguate_subject_column():
    """

    """
    mlmodel = MLModel()
    table = mlmodel.get_tables()[0]
    entities = disambiguate_subject_column(table)
    import ipdb; ipdb.set_trace()
