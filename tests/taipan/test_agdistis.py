"""Test for taipan.agdistis"""

from taipan.agdistis import AgdistisWrapper
from taipan.ml.model import MLModel

ENTITY = [{'start': 0, 'namedEntity': 'London', 'disambiguatedURL': 'http://dbpedia.org/resource/London', 'offset': 6}]
ROW_ENTITIES = [['http://dbpedia.org/resource/Jeff_Jahn'], [], []]
TO_FLATTEN = [{'start': 0, 'namedEntity': 'EUR', 'disambiguatedURL': 'http://dbpedia.org/resource/EUR,_Rome', 'offset': 3}]
FLATTENED = ['http://dbpedia.org/resource/EUR,_Rome']
TO_FLATTEN_NO_URL = [{'start': 0, 'namedEntity': '35.00', 'disambiguatedURL': None, 'offset': 5}]


def test_flatten_urls():
    agdistis_wrapper = AgdistisWrapper()
    flattened = agdistis_wrapper.flatten_urls(TO_FLATTEN)
    assert flattened == FLATTENED

    flattened = agdistis_wrapper.flatten_urls(TO_FLATTEN_NO_URL)
    assert flattened == []

def test_disambiguate_entity():
    agdistis_wrapper = AgdistisWrapper()
    entity = agdistis_wrapper.disambiguate_entity("London")
    assert entity == ENTITY

def test_disambiguate_table():
    mlmodel = MLModel()
    table = mlmodel.get_tables()[0]
    agdistis_wrapper = AgdistisWrapper()
    entities = agdistis_wrapper.disambiguate_table(table)
    assert len(entities) > 0
    assert entities[1] == [['http://dbpedia.org/resource/Australia'], [], []]

def test_disambiguate_row():
    mlmodel = MLModel()
    table = mlmodel.get_tables()[0]
    agdistis_wrapper = AgdistisWrapper()
    row = table.table[0]
    row_entities = agdistis_wrapper._disambiguate_row(row)
    assert row_entities == ROW_ENTITIES

def test_disambiguate_row_concat():
    mlmodel = MLModel()
    table = mlmodel.get_tables()[0]
    agdistis_wrapper = AgdistisWrapper()
    row = table.table[1]
    row_entities = agdistis_wrapper.disambiguate_row(row)
    row_entities_2 = agdistis_wrapper._disambiguate_row(row)
    assert row_entities == row_entities_2
    assert row_entities == [['http://dbpedia.org/resource/Australia'], [], []]
