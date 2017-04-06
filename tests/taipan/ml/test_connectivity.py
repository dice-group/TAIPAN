from taipan.ml.connectivity import ConnectivityCalculator
from taipan.ml.model import MLModel

C_CALC = ConnectivityCalculator()
MLMODEL = MLModel()

CONNECTIVITY_TABLE = [0.15, 0.13333333333333333, 0.016666666666666666]
def test_get_connectivity():
    table = MLMODEL.get_tables()[0]
    connectivity = C_CALC.get_connectivity(table)
    assert connectivity == CONNECTIVITY_TABLE

PROPERTIES = [
    {
        0: {0: [], 1: [], 2: []},
        1: {0: [], 1: [], 2: []},
        2: {0: [], 1: [], 2: []}
    },
    {
        0: {0: [], 1: ['http://dbpedia.org/property/deathPlace', 'http://dbpedia.org/ontology/nationality', 'http://dbpedia.org/ontology/populationPlace', 'http://dbpedia.org/ontology/deathPlace', 'http://dbpedia.org/ontology/country', 'http://dbpedia.org/property/birthPlace', 'http://dbpedia.org/property/nationality', 'http://dbpedia.org/property/origin', 'http://dbpedia.org/ontology/birthPlace', 'http://dbpedia.org/property/placeOfBirth', 'http://dbpedia.org/ontology/hometown', 'http://dbpedia.org/ontology/jurisdiction', 'http://dbpedia.org/property/placeOfDeath'], 2: []},
        1: {0: ['http://dbpedia.org/property/deathPlace', 'http://dbpedia.org/ontology/nationality', 'http://dbpedia.org/ontology/populationPlace', 'http://dbpedia.org/ontology/deathPlace', 'http://dbpedia.org/ontology/country', 'http://dbpedia.org/property/birthPlace', 'http://dbpedia.org/property/nationality', 'http://dbpedia.org/property/origin', 'http://dbpedia.org/ontology/birthPlace', 'http://dbpedia.org/property/placeOfBirth', 'http://dbpedia.org/ontology/hometown', 'http://dbpedia.org/ontology/jurisdiction', 'http://dbpedia.org/property/placeOfDeath'], 1: [], 2: []},
        2: {0: [], 1: [], 2: []}
    },
    {
        0: {0: [], 1: [], 2: []},
        1: {0: [], 1: [], 2: []},
        2: {0: [], 1: [], 2: []}
    },
    {
        0: {0: [], 1: [], 2: []},
        1: {0: [], 1: [], 2: []},
        2: {0: [], 1: [], 2: []}
    },
    {
        0: {0: [], 1: ['http://www.w3.org/2000/01/rdf-schema#comment', 'http://dbpedia.org/ontology/ground', 'http://dbpedia.org/ontology/regionServed', 'http://dbpedia.org/ontology/sourceCountry', 'http://dbpedia.org/ontology/type', 'http://www.w3.org/2000/01/rdf-schema#seeAlso', 'http://dbpedia.org/property/allegiance', 'http://dbpedia.org/ontology/locationCountry', 'http://dbpedia.org/property/ground', 'http://dbpedia.org/property/shipCountry', 'http://dbpedia.org/ontology/hometown', 'http://dbpedia.org/ontology/citizenship', 'http://dbpedia.org/property/country', 'http://dbpedia.org/property/areaServed', 'http://dbpedia.org/property/placeOfDeath', 'http://dbpedia.org/property/deathPlace', 'http://dbpedia.org/ontology/city', 'http://dbpedia.org/ontology/spokenIn', 'http://dbpedia.org/property/location', 'http://dbpedia.org/property/subdivisionName', 'http://dbpedia.org/ontology/stateOfOrigin', 'http://dbpedia.org/property/basinCountries', 'http://dbpedia.org/ontology/location', 'http://dbpedia.org/ontology/headquarter', 'http://dbpedia.org/ontology/birthPlace', 'http://dbpedia.org/ontology/place', 'http://dbpedia.org/property/regionServed', 'http://dbpedia.org/property/residence', 'http://dbpedia.org/ontology/nationality', 'http://dbpedia.org/ontology/abstract', 'http://dbpedia.org/ontology/country', 'http://dbpedia.org/ontology/residence', 'http://dbpedia.org/property/birthPlace', 'http://dbpedia.org/property/nationality', 'http://dbpedia.org/property/nationalOrigin', 'http://dbpedia.org/ontology/origin', 'http://dbpedia.org/property/placeOfBirth', 'http://dbpedia.org/property/locationCountry', 'http://dbpedia.org/ontology/deathPlace', 'http://dbpedia.org/property/states', 'http://dbpedia.org/property/shortDescription', 'http://dbpedia.org/property/headquarters'], 2: []},
        1: {0: ['http://www.w3.org/2000/01/rdf-schema#comment', 'http://dbpedia.org/ontology/ground', 'http://dbpedia.org/ontology/regionServed', 'http://dbpedia.org/ontology/sourceCountry', 'http://dbpedia.org/ontology/type', 'http://www.w3.org/2000/01/rdf-schema#seeAlso', 'http://dbpedia.org/property/allegiance', 'http://dbpedia.org/ontology/locationCountry', 'http://dbpedia.org/property/ground', 'http://dbpedia.org/property/shipCountry', 'http://dbpedia.org/ontology/hometown', 'http://dbpedia.org/ontology/citizenship', 'http://dbpedia.org/property/country', 'http://dbpedia.org/property/areaServed', 'http://dbpedia.org/property/placeOfDeath', 'http://dbpedia.org/property/deathPlace', 'http://dbpedia.org/ontology/city', 'http://dbpedia.org/ontology/spokenIn', 'http://dbpedia.org/property/location', 'http://dbpedia.org/property/subdivisionName', 'http://dbpedia.org/ontology/stateOfOrigin', 'http://dbpedia.org/property/basinCountries', 'http://dbpedia.org/ontology/location', 'http://dbpedia.org/ontology/headquarter', 'http://dbpedia.org/ontology/birthPlace', 'http://dbpedia.org/ontology/place', 'http://dbpedia.org/property/regionServed', 'http://dbpedia.org/property/residence', 'http://dbpedia.org/ontology/nationality', 'http://dbpedia.org/ontology/abstract', 'http://dbpedia.org/ontology/country', 'http://dbpedia.org/ontology/residence', 'http://dbpedia.org/property/birthPlace', 'http://dbpedia.org/property/nationality', 'http://dbpedia.org/property/nationalOrigin', 'http://dbpedia.org/ontology/origin', 'http://dbpedia.org/property/placeOfBirth', 'http://dbpedia.org/property/locationCountry', 'http://dbpedia.org/ontology/deathPlace', 'http://dbpedia.org/property/states', 'http://dbpedia.org/property/shortDescription', 'http://dbpedia.org/property/headquarters'], 1: [], 2: []},
        2: {0: [], 1: [], 2: []}
    }
]
CONNECTIVITY_CALC = [0.13333333333333333, 0.13333333333333333, 0.0]
def test_calculate_connectivity():
    connectivity = C_CALC.calculate_connectivity(PROPERTIES)
    assert CONNECTIVITY_CALC == connectivity
