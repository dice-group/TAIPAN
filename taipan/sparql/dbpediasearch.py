import re
import os
from SPARQLWrapper import SPARQLWrapper, JSON

from taipan.util import clear_string

DBPEDIA_SPARQL_ENDPOINT = os.environ.get("DBPEDIA_SPARQL_ENDPOINT", "http://dbpedia.org/sparql")
#DBPEDIA_SPARQL_ENDPOINT = os.environ.get("DBPEDIA_SPARQL_ENDPOINT", "http://dbpedia-live.openlinksw.com/sparql/")
DBPEDIA = SPARQLWrapper(DBPEDIA_SPARQL_ENDPOINT)
DBPEDIA.setReturnFormat(JSON)

def parse_results(results):
    properties = []
    for result in results:
        properties.append(result["property"]["value"])
    return properties

def uri_literal(s, o):
    properties = []
    properties.append(uri_literal_simple(s, o))
    properties.append(uri_literal_regex(s, o))
    properties.append(uri_literal_regex_reverse(s, o))
    properties = [item for sublist in properties for item in sublist]
    return list(set(properties))

def uri_uri(s, o):
    properties = []
    properties.append(uri_uri_simple(s, o))
    properties = [item for sublist in properties for item in sublist]
    return properties

def uri_uri_simple(s, o):
    DBPEDIA.setQuery(u"""
        SELECT DISTINCT ?property
        WHERE { <%s> ?property <%s> .}
    """ % (s, o,))
    results = DBPEDIA.query().convert()['results']['bindings']
    return parse_results(results)

def uri_literal_simple(s, o):
    o = clear_string(o)
    if o == "" or o == None:
        return []
    DBPEDIA.setQuery(u"""
        SELECT DISTINCT ?property
        WHERE { <%s> ?property "%s"@en .}
    """ % (s, o,))
    results = DBPEDIA.query().convert()['results']['bindings']
    return parse_results(results)

def uri_literal_regex(s, o):
    o = clear_string(o)
    if o == "" or o == None:
        return []
    DBPEDIA.setQuery(u"""
        SELECT DISTINCT ?property
        WHERE {
            <%s> ?property ?o .
            FILTER regex(?o, ".*%s.*", "i")
        }
    """ % (s, o,))
    results = DBPEDIA.query().convert()['results']['bindings']
    return parse_results(results)

def uri_literal_regex_reverse(s, o):
    o = clear_string(o)
    if o == "" or o == None:
        return []
    DBPEDIA.setQuery(u"""
        SELECT DISTINCT ?property
        WHERE {
            ?o ?property <%s> .
            FILTER regex(?o, ".*%s.*", "i")
        }
    """ % (s, o,))
    results = DBPEDIA.query().convert()['results']['bindings']
    return parse_results(results)
