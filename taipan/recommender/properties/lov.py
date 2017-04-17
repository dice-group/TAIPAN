import os
import requests

LOV_ENDPOINT = os.environ.get("LOV_ENDPOINT", "http://lov.okfn.org/dataset/lov/api/v2")
LOV_SEARCH_URI = LOV_ENDPOINT + "/term/search"

def get_table_properties(table, _type="dbpedia"):
    if _type != "dbpedia":
        raise NotImplemented
    header = table.table[0]
    properties = []
    for col_i, col in enumerate(header):
        col_properties = get_dbpedia_property(col)
        properties.append({
            "col_i": col_i,
            "properties": col_properties
        })
    return properties

def get_dbpedia_property(col):
    """
        Search for dbpedia properties in LOV
        Input: String
        Output: top 10 properties from LOV (URIs + prefixed notation)
    """
    params = {
        "q": col,
        "vocab": "dbpedia",
        "type": "property"
    }
    r = requests.get(LOV_SEARCH_URI, params=params)
    r.raise_for_status()
    properties = r.json()
    properties = [
        {
            'uri': _property['uri'][0],
            'prefixed_name': _property['prefixedName'][0],
            'score': _property['score']
        }
        for _property in properties['results']
    ]
    return properties
