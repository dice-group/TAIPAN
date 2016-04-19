import requests

class SimplePropertyRecommender(object):
    def __init__(self):
        pass

    def recommendPropertiesForTable(self, table):
        tableHeader = table.getHeader()
        properties = []
        for columnIndex, columnHeader in enumerate(tableHeader):
            columnProperties = self.lookupPropertiesLOV(columnHeader)
            properties.append({
                "columnIndex": columnIndex,
                "properties": columnProperties
            })
        return properties

    def lookupPropertiesLOV(self, columnHeader):
        """
            Search for dbpedia properties in LOV
            Input: String
            Output: top 10 properties from LOV (URIs + prefixed notation)
        """
        params = {
            "q": columnHeader,
            "vocab": "dbpedia",
            "type": "property"
        }
        lovSearchUri = "http://lov.okfn.org/dataset/lov/api/v2/term/search"
        r = requests.get(lovSearchUri, params=params)
        r.raise_for_status()
        if r.status_code == requests.codes.ok:
            properties = r.json()
            properties = [ {'uri': _property['uri'][0], 'prefixedName': _property['prefixedName'][0], 'score': _property['score']} for _property in properties['results'] ]
            return properties
