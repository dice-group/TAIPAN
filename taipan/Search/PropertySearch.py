from SPARQLWrapper import SPARQLWrapper, JSON
from taipan.Config.ExternalUris import dbpediaSparqlEndpointUri

class PropertySearchDbpediaSparql(object):
    """
        This class takes two entities (URI and URI/Literal)
        And returns all properties which (possibly) connects them
    """
    def __init__(self):
        self.dbpediaSparql = SPARQLWrapper(dbpediaSparqlEndpointUri)
        self.dbpediaSparql.setReturnFormat(JSON)

    def search(self, s, o):
        if(o.startswith('http')):
            return self.uriUriSimple(s, o)
        else:
            return self.uriLiteralSimple(s, o)

    def uriLiteralSearch(self, s, o):
        properties = []
        properties.append(self.uriLiteralSimple(s,o))
        properties.append(self.uriLiteralRegex(s,o))
        properties.append(self.uriLiteralPathRegex(s,o))
        properties.append(self.literalUriReversePathRegex(s,o))
        properties = [item for sublist in properties for item in sublist]
        return list(set(properties))

    def uriUriSearch(self, s, o):
        properties = []
        properties.append(self.uriUriSimple(s,o))
        return properties

    def uriUriSimple(self, s, o):
        self.dbpediaSparql.setQuery("""
            SELECT DISTINCT ?property
            WHERE { <%s> ?property <%s> .}
        """ % (s, o,))
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        return self.parseResults(results)

    def uriLiteralSimple(self, s, o):
        self.dbpediaSparql.setQuery("""
            SELECT DISTINCT ?property
            WHERE { <%s> ?property "%s"@en .}
        """ % (s, o,))
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        return self.parseResults(results)

    def uriLiteralRegex(self, s, o):
        self.dbpediaSparql.setQuery("""
            SELECT DISTINCT ?property
            WHERE {
                <%s> ?property ?o .
                FILTER regex(?o, ".*%s.*", "i")
            }
        """ % (s, o,))
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        return self.parseResults(results)

    def uriLiteralPathRegex(self, s, o):
        self.dbpediaSparql.setQuery("""
            SELECT DISTINCT ?property
            WHERE {
                <%s> ?property ?obj .
                ?obj ?p ?o .
                FILTER regex(?o, "%s", "i")
            }
        """ % (s, o,))
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        return self.parseResults(results)

    def literalUriReversePathRegex(self, s, o):
        self.dbpediaSparql.setQuery("""
            SELECT DISTINCT ?property
            WHERE {
                ?obj ?property <%s> .
                ?obj ?p ?o .
                FILTER regex(?o, "%s", "i")
            }
        """ % (s, o,))
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        return self.parseResults(results)

    def parseResults(self, results, variableName="property"):
        properties = []
        for result in results:
            properties.append(result[variableName]['value'])
        return properties
