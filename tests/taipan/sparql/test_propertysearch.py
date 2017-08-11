from taipan.entitysearch.agdistis import AgdistisWrapper
from taipan.ml.model import MLModel
from taipan.sparql.propertysearch import *

AGDISTIS = AgdistisWrapper()
MLMODEL = MLModel()

PROPERTIES_0 = {
    0: {0: [], 1: [], 2: []},
    1: {0: [], 1: [], 2: []},
    2: {0: [], 1: [], 2: []}
}

PROPERTIES_1 = {
    0: {0: [], 1: ['http://dbpedia.org/property/placeOfDeath', 'http://dbpedia.org/ontology/populationPlace', 'http://dbpedia.org/ontology/hometown', 'http://dbpedia.org/ontology/country', 'http://dbpedia.org/property/placeOfBirth', 'http://dbpedia.org/ontology/jurisdiction', 'http://dbpedia.org/property/deathPlace', 'http://dbpedia.org/property/birthPlace', 'http://dbpedia.org/property/origin', 'http://dbpedia.org/ontology/deathPlace', 'http://dbpedia.org/ontology/birthPlace', 'http://dbpedia.org/ontology/nationality', 'http://dbpedia.org/property/nationality'], 2: []},
    1: {0: ['http://dbpedia.org/property/placeOfDeath', 'http://dbpedia.org/ontology/populationPlace', 'http://dbpedia.org/ontology/hometown', 'http://dbpedia.org/ontology/country', 'http://dbpedia.org/property/placeOfBirth', 'http://dbpedia.org/ontology/jurisdiction', 'http://dbpedia.org/property/deathPlace', 'http://dbpedia.org/property/birthPlace', 'http://dbpedia.org/property/origin', 'http://dbpedia.org/ontology/deathPlace', 'http://dbpedia.org/ontology/birthPlace', 'http://dbpedia.org/ontology/nationality', 'http://dbpedia.org/property/nationality'], 1: [], 2: []},
    2: {0: [], 1: [], 2: []}
}

def test_find_properties():
    table = MLMODEL.get_tables()[0]
    entities = AGDISTIS.disambiguate_table(table)
    properties = find_properties(table, entities)
    assert properties[0] == PROPERTIES_0
    assert properties[1][0][1].sort() == PROPERTIES_1[0][1].sort()


A_COL_1 = "Germany"
B_COL_1 = "Berlin"
A_ENTITIES_1 = ['http://dbpedia.org/resource/Germany']
B_ENTITIES_1 = ['http://dbpedia.org/resource/Berlin']
PROPERTY_1 = ['http://dbpedia.org/ontology/language', 'http://dbpedia.org/property/city', 'http://dbpedia.org/property/stadium', 'http://dbpedia.org/property/birthPlace', 'http://dbpedia.org/property/capital', 'http://dbpedia.org/ontology/ground', 'http://dbpedia.org/ontology/country', 'http://dbpedia.org/ontology/place', 'http://dbpedia.org/ontology/spokenIn', 'http://dbpedia.org/ontology/locationCountry', 'http://dbpedia.org/ontology/hometown', 'http://dbpedia.org/property/nationalOrigin', 'http://dbpedia.org/property/place', 'http://dbpedia.org/property/recorded', 'http://dbpedia.org/ontology/headquarter', 'http://www.w3.org/2000/01/rdf-schema#seeAlso', 'http://dbpedia.org/property/locationCountry', 'http://dbpedia.org/property/country', 'http://dbpedia.org/property/nationality', 'http://dbpedia.org/ontology/city', 'http://dbpedia.org/ontology/nationality', 'http://dbpedia.org/ontology/broadcastArea', 'http://dbpedia.org/property/placeOfBirth', 'http://dbpedia.org/property/origin', 'http://dbpedia.org/ontology/abstract', 'http://dbpedia.org/ontology/capital', 'http://dbpedia.org/property/cityServed', 'http://dbpedia.org/ontology/birthPlace', 'http://dbpedia.org/ontology/recordedIn', 'http://dbpedia.org/ontology/homeStadium', 'http://dbpedia.org/ontology/location', 'http://dbpedia.org/property/location', 'http://dbpedia.org/ontology/origin', 'http://dbpedia.org/property/region', 'http://dbpedia.org/ontology/foundationPlace', 'http://www.w3.org/2000/01/rdf-schema#comment', 'http://dbpedia.org/ontology/residence', 'http://www.w3.org/2002/07/owl#sameAs', 'http://dbpedia.org/property/residence', 'http://dbpedia.org/property/states', 'http://dbpedia.org/property/headquarters']
def test_find_property():
    properties = find_property(A_COL_1, B_COL_1, A_ENTITIES_1, B_ENTITIES_1)
    assert properties.sort() == PROPERTY_1.sort()
