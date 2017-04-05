import collections
#from memorize import Memorize

from taipan.sparql.dbpediasearch import uri_literal, uri_uri

#@Memorize
def find_properties(self, table, entities):
    table_data = table.table

    relations = []
    for row_i, row in enumerate(table_data):
        row_rels = collections.defaultdict(dict)
        for col_i, col in enumerate(row):
            entity = entities[row_i][col_i]
            for b_col_i, b_col in enumerate(row[col_i:]):
                b_col_i = col_i + b_col_i
                if(row[col_i] == row[b_col_i]):
                    rowRels[col_i][b_col_i] = []
                else:
                    rel = self.find_properties(
                        col,
                        b_col,
                        entities[row_i][col_i],
                        entities[row_i][b_col_i]
                    )
                    row_rels[col_i][b_col_i] = rel
                    row_rels[b_col_i][col_i] = rel
        relations.append(dict(row_rels))
    return relations

#@Memorize
def find_property(self, col, b_col, entities, b_entities):
    properties = []

    if(len(entities) > 0):
        for entity in entities:
            properties.append(uri_literal(entity, b_col))
    elif(len(b_entities) > 0):
        for b_entity in b_entities:
            properties.append(uri_literal(b_entity, col))
    elif(len(entities) > 0 and len(b_entities) > 0):
        for entity in entities:
            for b_entity in b_entities:
                properties.append(uri_uri(entity, b_entity))

    properties = [prop for sublist in properties for prop in sublist]
    return list(set(properties))
