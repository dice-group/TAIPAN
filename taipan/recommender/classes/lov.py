import os
import requests

LOV_ENDPOINT = os.environ.get("LOV_ENDPOINT", "http://lov.okfn.org/dataset/lov/api/v2")
LOV_SEARCH_URI = LOV_ENDPOINT + "/term/search"

def get_table_class(search_term):
    """
        Input: String
        Output: top 10 classes from LOV (URIs + prefixed notation)
    """
    params = {
        "q": search_term,
        #"vocab": "dbpedia",
        "type": "class"
    }
    if not search_term:
        return []
    r = requests.get(LOV_SEARCH_URI, params=params)
    r.raise_for_status()
    classes = r.json()
    classes = [
        {
            'uri': _class['uri'][0],
            'prefixed_name': _class['prefixedName'][0],
            'score': _class['score']
        }
        for _class in classes['results']
    ]
    return classes
