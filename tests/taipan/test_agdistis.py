"""Test for taipan.agdistis"""

from taipan.agdistis import AgdistisWrapper
from taipan.ml.model import MLModel

ENTITY = [{'start': 0, 'namedEntity': 'London', 'disambiguatedURL': 'http://dbpedia.org/resource/London', 'offset': 6}]
TABLE_ENTITIES = [[['http://dbpedia.org/resource/Jeff_Jahn'], [], []], [['http://dbpedia.org/resource/Australia'], [], []], [['http://dbpedia.org/resource/Bangladesh'], ['http://dbpedia.org/resource/United_States_Department_of_Defense'], []], [['http://dbpedia.org/resource/Cambodia'], ['http://dbpedia.org/resource/United_States_Department_of_Defense'], []], [['http://dbpedia.org/resource/Canada'], ['http://dbpedia.org/resource/Computer-aided_design'], []], [['http://dbpedia.org/resource/France_2'], ['http://dbpedia.org/resource/EUR,_Rome'], []], [['http://dbpedia.org/resource/Germany'], ['http://dbpedia.org/resource/EUR,_Rome'], []], [['http://dbpedia.org/resource/Hong_Kong'], [], []], [['http://dbpedia.org/resource/India'], ['http://dbpedia.org/resource/Institute_for_Nuclear_Research'], []], [['http://dbpedia.org/resource/Indonesia'], ['http://dbpedia.org/resource/United_States_Department_of_Defense'], []], [['http://dbpedia.org/resource/Italy'], ['http://dbpedia.org/resource/EUR,_Rome'], []], [['http://dbpedia.org/resource/Japan'], [], []], [['http://dbpedia.org/resource/Korea'], ['http://dbpedia.org/resource/KRW'], []], [['http://dbpedia.org/resource/Malaysia'], ['http://dbpedia.org/resource/Myrtle_Beach,_South_Carolina'], []], [['http://dbpedia.org/resource/Nepal'], ['http://dbpedia.org/resource/United_States_Department_of_Defense'], []], [['http://dbpedia.org/resource/New_Zealand'], [], []], [['http://dbpedia.org/resource/Papua_New_Guinea'], ['http://dbpedia.org/resource/Pasukan_Gerakan_Khas'], []], [[], ['http://dbpedia.org/resource/Central_New_York'], []], [['http://dbpedia.org/resource/Philippines'], ['http://dbpedia.org/resource/United_States_Department_of_Defense'], []], [['http://dbpedia.org/resource/Portugal'], ['http://dbpedia.org/resource/EUR,_Rome'], []]]
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
    assert entities == TABLE_ENTITIES

def test_disambiguate_row():
    mlmodel = MLModel()
    table = mlmodel.get_tables()[0]
    agdistis_wrapper = AgdistisWrapper()
    row = table.table[0]
    row_entities = agdistis_wrapper.disambiguate_row(row)
    assert row_entities == ROW_ENTITIES
