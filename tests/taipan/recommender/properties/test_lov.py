from taipan.recommender.properties.lov import get_dbpedia_property, get_table_properties
from taipan.ml.model import MLModel

MLMODEL = MLModel()

_PROPERTY = {
    'prefixed_name': 'dbpedia-owl:populationTotal',
    'score': 0.9519177,
    'uri': 'http://dbpedia.org/ontology/populationTotal'
}

_COLUMN =  {
    'col_i': 1,
    'properties': [
        {
            'prefixed_name': 'dbpedia-owl:currency',
            'score': 2.103575,
            'uri': 'http://dbpedia.org/ontology/currency'
        },
        {
            'prefixed_name': 'dbpedia-owl:currencyCode',
            'score': 1.3147343,
            'uri': 'http://dbpedia.org/ontology/currencyCode'
        }
    ]
}


def test_get_dbpedia_property():
    term = "population"
    properties = get_dbpedia_property(term)
    assert 'prefixed_name' in properties[0]
    assert 'score' in properties[0]
    assert 'uri' in properties[0]

def test_get_table_properties():
    table = MLMODEL.get_tables()[0]
    table_properties = get_table_properties(table)
    assert 'col_i' in table_properties[0]
    assert 'properties' in table_properties[0]
