import os

from taipan.pathes import TABLES_DIR
from taipan.generictable import GenericTable
from taipan.mapper.properties.connectivity import map_atomic_table_property, \
    get_all_dict_values

TEST_FILENAME = os.path.join(TABLES_DIR, "cardinals_table.csv")

def test_map_atomic_table_property():
    table = GenericTable(TEST_FILENAME)
    table.init()
    _property = map_atomic_table_property(table)
    assert _property == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

def test_get_all_dict_values():
    _dict = {0:
             {
                 0: [],
                 1: [
                     'http://purl.org/dc/terms/description',
                     'http://dbpedia.org/ontology/wikiPageWikiLink',
                     'http://dbpedia.org/ontology/abstract',
                     'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                     'http://www.w3.org/2000/01/rdf-schema#comment',
                     'http://dbpedia.org/property/title',
                     'http://purl.org/dc/terms/subject']},
             1: {0: [
                 'http://purl.org/dc/terms/description',
                 'http://dbpedia.org/ontology/wikiPageWikiLink',
                 'http://dbpedia.org/ontology/abstract',
                 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                 'http://www.w3.org/2000/01/rdf-schema#comment',
                 'http://dbpedia.org/property/title',
                 'http://purl.org/dc/terms/subject'],
                 1: []}}
    result = []
    values = get_all_dict_values(_dict, result)
    assert len(values) == 14
