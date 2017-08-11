"""DBpedia lookup wrapper."""

import requests
from xml.dom.minidom import parseString

KEYWORD_SEARCH_URI = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch"

def lookup_dbpedia_entity(entity_string, _class=None):
    if string_only_contain(entity_string, "1234567890%.&#;") or entity_string == "NULL"\
        or entity_string == "null" or len(entity_string) < 3:
        return []

    params = {
        "QueryString": entity_string,
        "MaxHits": 5
    }
    if _class:
        params["QueryClass"] = _class
    r = requests.get(KEYWORD_SEARCH_URI, params=params)
    r.raise_for_status()
    xml_entities = parseString(r.content)
    result_nodes = xml_entities.getElementsByTagName("Result")
    if len(result_nodes) > 0:
        first_uri_node = result_nodes[0].getElementsByTagName("URI")[0]
        return [first_uri_node.firstChild.data]
    else:
        return []

def disambiguate_row(row):
    entities = []
    for cell_i, cell in enumerate(row):
        entities.append(lookup_dbpedia_entity(cell))
    return entities

def disambiguate_table(table):
    entities = []
    for row in table.table:
        entities.append(disambiguate_row(row))
    return entities

def disambiguate_table_subject_column_only(table):
    entities = []
    for row in table.table:
        row_entities = []
        for cell_i, cell in enumerate(row):
            if cell_i == table.subject_column:
                row_entities.append(lookup_dbpedia_entity(cell))
            else:
                row_entities.append([])
        entities.append(row_entities)
    return entities


def string_only_contain(_string, characters):
    for char in _string:
        if not char in characters:
            return False
    return True
