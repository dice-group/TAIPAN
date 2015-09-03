import unittest

from taipan.Utils.Sampling import Sampler
from taipan.Relational.Parsers import MannheimTable
from taipan.Search.PropertySearch import PropertySearch

class PropertySearchTestCase(unittest.TestCase):
    def setUp(self):
        self.propertySearch = PropertySearch()

    def testSearchPropertiesSparqlUriUri(self):
        s = "http://dbpedia.org/resource/Batman_&_Robin_(film)";
        o = "http://dbpedia.org/resource/Akiva_Goldsman";
        properties = self.propertySearch.searchPropertiesSparql(s, o)
        propertyShouldExist = "http://dbpedia.org/ontology/writer"
        self.assertTrue(propertyShouldExist in properties, msg="Property %s should be in %s" %(propertyShouldExist, properties,))

    def testSearchPropertiesSparqlUriLiteral(self):
        s = "http://dbpedia.org/resource/Batman_&_Robin_(film)";
        o = "Batman & Robin";
        properties = self.propertySearch.searchPropertiesSparql(s, o)
        propertyShouldExist = "http://dbpedia.org/property/name"
        self.assertTrue(propertyShouldExist in properties, msg="Property %s should be in %s" %(propertyShouldExist, properties,))

        s = "http://dbpedia.org/resource/Batman_&_Robin_(film)";
        o = "English";
        properties = self.propertySearch.searchPropertiesSparql(s, o)
        propertyShouldExist = "http://dbpedia.org/property/language"
        self.assertTrue(propertyShouldExist in properties, msg="Property %s should be in %s" %(propertyShouldExist, properties,))
