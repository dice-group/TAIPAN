"""Entity search from a SPARQL endpoint."""

import os
from SPARQLWrapper import SPARQLWrapper, JSON

from taipan.util import clear_string

DBPEDIA_SPARQL_ENDPOINT = os.environ.get("DBPEDIA_SPARQL_ENDPOINT", "http://dbpedia.org/sparql")
#DBPEDIA_SPARQL_ENDPOINT = os.environ.get("DBPEDIA_SPARQL_ENDPOINT", "http://dbpedia-live.openlinksw.com/sparql/")
DBPEDIA = SPARQLWrapper(DBPEDIA_SPARQL_ENDPOINT)
DBPEDIA.setReturnFormat(JSON)


def retrieve_entity_filter(entity_label):
    """
        Timeouts
    """
    DBPEDIA.setQuery(u"""
        SELECT DISTINCT ?s
        WHERE {
            ?s ?p ?o .
            FILTER regex(?o, ".*%s.*", "i")
        } LIMIT 5
    """ % (entity_label,))
    results = DBPEDIA.query().convert()['results']['bindings']
    return results
