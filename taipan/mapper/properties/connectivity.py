from collections import Counter

from taipan.sparql.propertysearch import find_properties
from taipan.dbpedialookup import disambiguate_table
from taipan.mapper.properties.stoplist import DBPEDIA_STOPLIST

def map_table_properties_connectivity(table, rows_to_analyze=10):
    table.trim_table(rows_to_analyze)
    entities = disambiguate_table(table)
    properties = find_properties(table, entities)
    property_groups = group_properties_by_column(properties)
    for property_group in property_groups:
        counter = Counter(property_groups[property_group])
        property_groups[property_group] = get_top_property(counter)
    return property_groups

def group_properties_by_column(properties):
    result = {}
    for row in properties:
        hashes = []
        for column in row:
            for other_column in row[column]:
                if column == other_column:
                    continue
                if column != 0:
                    continue
                _values = row[column][other_column]
                _k = [column, other_column]
                _k.sort()
                _k = "_".join(str(x) for x in _k)
                if not _k in hashes:
                    hashes.append(_k)
                    if not _k in result:
                        result[_k] = []
                        for _value in _values:
                            if not _value in DBPEDIA_STOPLIST:
                                result[_k].append(_value)
                    else:
                        for _value in _values:
                            if not _value in DBPEDIA_STOPLIST:
                                result[_k].append(_value)
    return result

def get_top_property(properties_counter):
    _prop = properties_counter.most_common(1)
    if _prop:
        return _prop[0][0]
    else:
        return None

def flatten_properties(properties):
    flat_properties = []
    while True:
        if len(properties) > 0:
            flat_properties += get_all_dict_values(properties.pop())
        else:
            break
    return flat_properties

def get_all_dict_values(_dict, result=[]):
    if isinstance(_dict, list):
        result += _dict
    else:
        for (k, v) in _dict.items():
            get_all_dict_values(v, result)
    return result
