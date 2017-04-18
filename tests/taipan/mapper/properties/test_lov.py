import os

from taipan.pathes import TABLES_DIR
from taipan.generictable import GenericTable
from taipan.mapper.properties.lov import map_table_properties

TEST_FILENAME = os.path.join(TABLES_DIR, "000ec48b-f25f-47ef-af12-1f897207cdb4.csv")

MAPPED_PROPERTIES = [
 {'prefixed_name': 'dbpedia-owl:birthPlace',
  'score': 1,
  'uri': 'http://dbpedia.org/ontology/birthPlace'},
 {'prefixed_name': 'dbpedia-owl:birthPlace',
  'score': 1,
  'uri': 'http://dbpedia.org/ontology/birthPlace'},
 {'prefixed_name': 'dbpedia-owl:recordLabel',
  'score': 2.0589364,
  'uri': 'http://dbpedia.org/ontology/recordLabel'}
]

def test_map_table_properties():
    table = GenericTable(TEST_FILENAME)
    properties = map_table_properties(table)
    assert properties == MAPPED_PROPERTIES
