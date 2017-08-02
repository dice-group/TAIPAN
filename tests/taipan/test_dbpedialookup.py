"""Test for taipan.dbpedialookup"""

from taipan.dbpedialookup import lookup_dbpedia_entity, disambiguate_table
from taipan.ml.model import MLModel


def test_lookup_dbpedia_entity():
    _entity = lookup_dbpedia_entity("Berlin")
    assert _entity == ["http://dbpedia.org/resource/Berlin"]


def test_lookup_dbpedia_entity_dont_exist():
    _entity = lookup_dbpedia_entity("fdsoiajoij foidjsafp odij pfoij")
    assert _entity == []

TABLE_ENTITIES = [[['http://dbpedia.org/resource/Portuguese_language'], ['http://dbpedia.org/resource/United_States_dollar'], []],
 [['http://dbpedia.org/resource/Australia'], ['http://dbpedia.org/resource/Australian_dollar'], []],
 [['http://dbpedia.org/resource/Bangladesh'], ['http://dbpedia.org/resource/United_States_dollar'], []],
 [['http://dbpedia.org/resource/Cambodia'], ['http://dbpedia.org/resource/United_States_dollar'], []],
 [['http://dbpedia.org/resource/Canada'], ['http://dbpedia.org/resource/Canadian_dollar'], []],
 [['http://dbpedia.org/resource/France'], ['http://dbpedia.org/resource/Euro'], []],
 [['http://dbpedia.org/resource/Germany'], ['http://dbpedia.org/resource/Euro'], []],
 [['http://dbpedia.org/resource/Hong_Kong'], ['http://dbpedia.org/resource/Hong_Kong_dollar'], []],
 [['http://dbpedia.org/resource/India'], ['http://dbpedia.org/resource/Indian_rupee'], []],
 [['http://dbpedia.org/resource/Indonesia'], ['http://dbpedia.org/resource/United_States_dollar'], ['http://dbpedia.org/resource/Confederate_States_of_America_dollar']],
 [['http://dbpedia.org/resource/Italy'], ['http://dbpedia.org/resource/Euro'], []],
 [['http://dbpedia.org/resource/Japan'], ['http://dbpedia.org/resource/Japanese_yen'], []],
 [['http://dbpedia.org/resource/South_Korea'], ['http://dbpedia.org/resource/South_Korean_won'], []],
 [['http://dbpedia.org/resource/Malaysia'], ['http://dbpedia.org/resource/Malaysian_ringgit'], []],
 [['http://dbpedia.org/resource/Nepal'], ['http://dbpedia.org/resource/United_States_dollar'], []],
 [['http://dbpedia.org/resource/New_Zealand'], ['http://dbpedia.org/resource/New_Zealand_dollar'], []],
 [['http://dbpedia.org/resource/Papua_New_Guinea'], ['http://dbpedia.org/resource/Papua_New_Guinean_kina'], ['http://dbpedia.org/resource/Confederate_States_of_America_dollar']],
 [[], ['http://dbpedia.org/resource/Renminbi'], []],
 [['http://dbpedia.org/resource/Philippines'], ['http://dbpedia.org/resource/United_States_dollar'], []],
 [['http://dbpedia.org/resource/Portugal'], ['http://dbpedia.org/resource/Euro'], []]]


def test_disambiguate_table():
    mlmodel = MLModel()
    table = mlmodel.get_tables()[0]
    entities = disambiguate_table(table)
    assert entities == TABLE_ENTITIES
