import unittest

from taipan.Utils.Sampling import Sampler
from taipan.Relational.Parsers import MannheimTable
from taipan.Search.PropertySearch import PropertySearchDbpediaSparql

class PropertySearchTestCase(unittest.TestCase):
    def setUp(self):
        self.propertySearch = PropertySearchDbpediaSparql()

    def testUriUri(self):
        s = "http://dbpedia.org/resource/Batman_&_Robin_(film)";
        o = "http://dbpedia.org/resource/Akiva_Goldsman";
        properties = self.propertySearch.search(s, o)
        propertyShouldExist = "http://dbpedia.org/ontology/writer"
        self.assertTrue(propertyShouldExist in properties, msg="Property %s should be in %s" %(propertyShouldExist, properties,))

    def testUriLiteral(self):
        s = "http://dbpedia.org/resource/Batman_&_Robin_(film)";
        o = "Batman & Robin";
        properties = self.propertySearch.search(s, o)
        propertyShouldExist = "http://xmlns.com/foaf/0.1/name"
        self.assertTrue(propertyShouldExist in properties, msg="Property %s should be in %s" %(propertyShouldExist, properties,))

        s = "http://dbpedia.org/resource/Batman_&_Robin_(film)";
        o = "English";
        properties = self.propertySearch.search(s, o)
        propertyShouldExist = "http://dbpedia.org/property/language"
        self.assertTrue(propertyShouldExist in properties, msg="Property %s should be in %s" %(propertyShouldExist, properties,))

    def testUriLiteralRegex(self):
        s = "http://dbpedia.org/resource/Austria";
        o = "101.4";
        properties = self.propertySearch.uriLiteralRegex(s, o)
        propertyShouldExist = "http://dbpedia.org/ontology/PopulatedPlace/populationDensity"
        self.assertTrue(propertyShouldExist in properties, msg="Property %s should be in %s" %(propertyShouldExist, properties,))

    def testUriLiteralPathRegex(self):
        s = "http://dbpedia.org/resource/Austria";
        o = "2004";
        properties = self.propertySearch.uriLiteralPathRegex(s, o)
        propertyShouldExist = "http://dbpedia.org/ontology/leader"
        self.assertTrue(propertyShouldExist in properties, msg="Property %s should be in %s" %(propertyShouldExist, properties,))

    def testLiteralUriReversePathRegex(self):
        s = "http://dbpedia.org/resource/Austria";
        o = "2004";
        properties = self.propertySearch.literalUriReversePathRegex(s, o)
        propertyShouldExist = "http://dbpedia.org/property/venue"
        self.assertTrue(propertyShouldExist in properties, msg="Property %s should be in %s" %(propertyShouldExist, properties,))
