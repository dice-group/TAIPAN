"""Test for taipan.table"""

from taipan.sparql.dbpediasearch import *

URI_A = "http://dbpedia.org/resource/Berlin"
URI_B = "http://dbpedia.org/resource/Germany"
LITERAL_A = "Berliner"
LITERAL_B = "capital"


URI_URI_PROPERTIES = ['http://www.w3.org/2000/01/rdf-schema#seeAlso', 'http://dbpedia.org/ontology/country']
def test_uri_uri_simple():
    properties = uri_uri_simple(URI_A, URI_B)
    assert properties == URI_URI_PROPERTIES


URI_LITERAL_A_PROPERTIES = ['http://dbpedia.org/ontology/demonym', 'http://dbpedia.org/property/populationDemonym']
def test_uri_literal_simple():
    properties = uri_literal_simple(URI_A, LITERAL_A)
    assert properties == URI_LITERAL_A_PROPERTIES


URI_LITERAL_B_PROPERTIES = ['http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2000/01/rdf-schema#comment', 'http://dbpedia.org/ontology/abstract', 'http://purl.org/dc/terms/subject']
def test_uri_literal_regex():
    properties = uri_literal_regex(URI_A, LITERAL_B)
    assert len(properties) > 0
    assert properties[0].startswith('http')
    #assert properties == URI_LITERAL_B_PROPERTIES

URI_LITERAL_B_PROPERTIES_REVERSE = ['http://dbpedia.org/ontology/location', 'http://dbpedia.org/ontology/wikiPageRedirects', 'http://dbpedia.org/property/location']
def test_uri_literal_regex_reverse():
    properties = uri_literal_regex_reverse(URI_A, LITERAL_B)
    #assert properties == URI_LITERAL_B_PROPERTIES_REVERSE
    assert len(properties) > 0
    assert properties[0].startswith('http')


URI_LITERAL_ALL_PROPERTIES = ['http://dbpedia.org/property/birthPlace', 'http://dbpedia.org/property/location', 'http://dbpedia.org/ontology/city', 'http://dbpedia.org/property/populationDemonym', 'http://dbpedia.org/ontology/demonym', 'http://dbpedia.org/property/city', 'http://dbpedia.org/ontology/birthPlace', 'http://dbpedia.org/ontology/locationCity', 'http://dbpedia.org/ontology/location', 'http://dbpedia.org/ontology/headquarter', 'http://dbpedia.org/ontology/nonFictionSubject', 'http://dbpedia.org/ontology/regionServed', 'http://dbpedia.org/ontology/deathPlace', 'http://dbpedia.org/property/placeOfBirth', 'http://dbpedia.org/property/headquarters']
def test_uri_literal():
    properties = uri_literal(URI_A, LITERAL_A)
    assert properties.sort() == URI_LITERAL_ALL_PROPERTIES.sort()


URI_URI_ALL_PROPERTIES = ['http://www.w3.org/2000/01/rdf-schema#seeAlso', 'http://dbpedia.org/ontology/country']
def test_uri_uri():
    properties = uri_uri(URI_A, URI_B)
    assert properties == URI_URI_ALL_PROPERTIES
