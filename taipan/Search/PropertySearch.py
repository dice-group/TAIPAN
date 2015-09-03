from SPARQLWrapper import SPARQLWrapper, JSON
from taipan.Config.ExternalUris import dbpediaSparqlEndpointUri

class PropertySearch(object):
    """
        This class takes two entities (URI and URI/Literal)
        And returns all properties which (possibly) connects them
    """
    def __init__(self):
        self.dbpediaSparql = SPARQLWrapper(dbpediaSparqlEndpointUri)
        self.dbpediaSparql.setReturnFormat(JSON)

    def searchPropertiesSparql(self, s, o):
        #TODO: smart switch to detect if o is a URL or Literal
        if(o.startswith('http')):
            return self.searchPropertiesSparqlUriUri(s, o)
        else:
            return self.searchPropertiesSparqlUriLiteral(s, o)

    def searchPropertiesSparqlUriUri(self, s, o):
        self.dbpediaSparql.setQuery("""
            SELECT ?property
            WHERE { <%s> ?property <%s> .}
        """ % (s, o,))
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        properties = []
        for result in results:
            properties.append(result['property']['value'])
        return properties

    def searchPropertiesSparqlUriLiteral(self, s, o):
        self.dbpediaSparql.setQuery("""
            SELECT ?property
            WHERE { <%s> ?property "%s"@en .}
        """ % (s, o,))
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        properties = []
        for result in results:
            properties.append(result['property']['value'])
        return properties
