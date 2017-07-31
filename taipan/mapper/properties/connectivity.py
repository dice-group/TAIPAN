from collections import Counter

from taipan.sparql.propertysearch import find_properties
from taipan.agdistis import AgdistisWrapper

AGDISTIS = AgdistisWrapper()
def map_table_properties_connectivity(table, rows_to_analyze=10):
    table.table = table.table[:rows_to_analyze]
    entities = AGDISTIS.disambiguate_table(table)
    properties = find_properties(table, entities)
    flat_properties = []
    while True:
        if len(properties) > 0:
            flat_properties += get_all_dict_values(properties.pop())
        else:
            break
    # get mode
    properties_counter = Counter(flat_properties)
    return properties_counter.most_common(1)[0][0]

def get_all_dict_values(_dict, result=[]):
    if isinstance(_dict, list):
        result += _dict
    else:
        for (k, v) in _dict.items():
            get_all_dict_values(v, result)
    return result
