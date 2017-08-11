"""TAIPAN entity search implementation."""

from taipan.entitysearch.dbpedialookup import lookup_dbpedia_entity, \
    disambiguate_table_subject_column_only

def disambiguate_subject_column(table):
    """
        Pick the subject column
        and look for all the labels in the column
    """
    entities_column = []
    _t = table.table
    for row in _t:
        for cell_i, cell in enumerate(row):
            if cell_i == table.subject_column:
                entities_column.append(lookup_dbpedia_entity(cell))
    return entities_column
