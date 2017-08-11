"""Test for taipan.agdistis"""

from os.path import isfile, join

from taipan.entitysearch.agdistis import AgdistisWrapper
from taipan.ml.model import MLModel
from taipan.generictable import GenericTable

ENTITY = [{'start': 0, 'namedEntity': 'London', 'disambiguatedURL': 'http://dbpedia.org/resource/London', 'offset': 6}]
ROW_ENTITIES = [['http://dbpedia.org/resource/Jeff_Jahn'], [], []]
TO_FLATTEN = [{'start': 0, 'namedEntity': 'EUR', 'disambiguatedURL': 'http://dbpedia.org/resource/EUR,_Rome', 'offset': 3}]
FLATTENED = ['http://dbpedia.org/resource/EUR,_Rome']
TO_FLATTEN_NO_URL = [{'start': 0, 'namedEntity': '35.00', 'disambiguatedURL': None, 'offset': 5}]

agdistis_wrapper = AgdistisWrapper()
mlmodel = MLModel()
table = mlmodel.get_tables()[0]

def test_flatten_urls():
    flattened = agdistis_wrapper.flatten_urls(TO_FLATTEN)
    assert flattened == FLATTENED

    flattened = agdistis_wrapper.flatten_urls(TO_FLATTEN_NO_URL)
    assert flattened == []

def test_disambiguate_entity():
    entity = agdistis_wrapper.disambiguate_entity("London")
    assert entity == ENTITY

def test_disambiguate_table():
    entities = agdistis_wrapper.disambiguate_table(table)
    assert len(entities) > 0
    assert entities[1] == [['http://dbpedia.org/resource/Australia'], [], []]

def test_disambiguate_row():
    row = table.table[1]
    row_entities = agdistis_wrapper._disambiguate_row(row)
    assert len(row_entities) > 0

def test_disambiguate_row_concat():
    row = table.table[1]
    row_entities = agdistis_wrapper.disambiguate_row(row)
    row_entities_2 = agdistis_wrapper._disambiguate_row(row)
    assert row_entities == row_entities_2
    assert row_entities == [['http://dbpedia.org/resource/Australia'], [], []]

def test_table_case():
    from taipan.pathes import TABLES_DIR
    _id = "34041816_1_4749054164534706977.csv"
    _table = GenericTable(filename=join(TABLES_DIR, _id), _id=_id)
    _table.init()
    row = _table.table[1]
    concat_dis = agdistis_wrapper.disambiguate_row(row)
    cell_dis = agdistis_wrapper._disambiguate_row(row)
