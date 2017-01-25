import re
from SPARQLWrapper import SPARQLWrapper, JSON
from taipan.Config.ExternalUris import dbpediaSparqlEndpointUri
from taipan.Logging.Logger import Logger

class PropertySearchDbpediaSparql(object):
    """
        This class takes two entities (URI and URI/Literal)
        And returns all properties which (possibly) connects them
    """
    def __init__(self):
        self.logger = Logger().getLogger(__name__)
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
        properties.append(self.uriLiteralRegexReverse(s,o))
        properties = [item for sublist in properties for item in sublist]
        return list(set(properties))

    def uriUriSearch(self, s, o):
        properties = []
        properties.append(self.uriUriSimple(s,o))
        return properties

    def uriUriSimple(self, s, o):
        self.dbpediaSparql.setQuery(u"""
            SELECT DISTINCT ?property
            WHERE { <%s> ?property <%s> .}
        """ % (s, o,))
        self.queryDebugMessage("uriUriSimple", s, o, self.dbpediaSparql.queryString)
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        return self.parseResults(results)

    def uriLiteralSimple(self, s, o):
        o = self.clearLiteral(o)
        if o == "" or o == None:
            return []
        self.dbpediaSparql.setQuery(u"""
            SELECT DISTINCT ?property
            WHERE { <%s> ?property "%s"@en .}
        """ % (s, o,))
        self.queryDebugMessage("uriLiteralSimple", s, o, self.dbpediaSparql.queryString)
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        return self.parseResults(results)

    def uriLiteralRegex(self, s, o):
        o = self.clearLiteral(o)
        if o == "" or o == None:
            return []
        self.dbpediaSparql.setQuery(u"""
            SELECT DISTINCT ?property
            WHERE {
                <%s> ?property ?o .
                FILTER regex(?o, ".*%s.*", "i")
            }
        """ % (s, o,))
        self.queryDebugMessage("uriLiteralRegex", s, o, self.dbpediaSparql.queryString)
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        return self.parseResults(results)

    def uriLiteralRegexReverse(self, s, o):
        o = self.clearLiteral(o)
        if o == "" or o == None:
            return []
        self.dbpediaSparql.setQuery(u"""
            SELECT DISTINCT ?property
            WHERE {
                ?o ?property <%s> .
                FILTER regex(?o, ".*%s.*", "i")
            }
        """ % (s, o,))
        self.queryDebugMessage("uriLiteralRegexReverse", s, o, self.dbpediaSparql.queryString)
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        return self.parseResults(results)

    def uriLiteralPathRegex(self, s, o):
        """
            Due to small diameter of a graph looking for any pathes will lead to noise. Most likely F-measure will drop if used together with simple property search.
        """
        o = self.clearLiteral(o)
        if o == "" or o == None:
            return []
        self.dbpediaSparql.setQuery(u"""
            SELECT DISTINCT ?property
            WHERE {
                <%s> ?property ?obj .
                ?obj ?p ?o .
                FILTER regex(?o, "%s", "i")
            }
        """ % (s, o,))
        self.queryDebugMessage("uriLiteralPathRegex", s, o, self.dbpediaSparql.queryString)
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        return self.parseResults(results)

    def literalUriPathRegexReverse(self, s, o):
        o = self.clearLiteral(o)
        if o == "" or o == None:
            return []
        self.dbpediaSparql.setQuery(u"""
            SELECT DISTINCT ?property
            WHERE {
                ?obj ?property <%s> .
                ?obj ?p ?o .
                FILTER regex(?o, "%s", "i")
            }
        """ % (s, o,))
        self.queryDebugMessage("literalUriPathRegexReverse", s, o, self.dbpediaSparql.queryString)
        results = self.dbpediaSparql.query().convert()['results']['bindings']
        return self.parseResults(results)

    def clearLiteral(self, string):
        string = re.sub('[{}|*?()\[\]!-"]', '', string)
        string = re.sub('&nbsp;', '', string)
        string = string.strip()
        return string

    def queryDebugMessage(self, functionName, s, o, queryString):
        self.logger.debug("%s ?s: %s ?o: %s" %(functionName, s, o, ))
        self.logger.debug("SPARQL query: %s" %(queryString, ))

    def parseResults(self, results, variableName="property"):
        properties = []
        for result in results:
            properties.append(result[variableName]['value'])
        return properties
