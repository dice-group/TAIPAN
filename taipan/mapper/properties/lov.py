from taipan.recommender.properties.lov import get_table_properties

def map_table_properties(table):
    recommended_properties = get_table_properties(table)
    mapped_properties = [None]*len(recommended_properties)
    for col in recommended_properties:
        mapped_properties[col["col_i"]] = sorted(col['properties'], key=lambda x: x['score'], reverse=True)[0]
    return mapped_properties
