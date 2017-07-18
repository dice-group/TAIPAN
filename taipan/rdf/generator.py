import os
from urllib.parse import quote_plus

from rdflib import Graph, Literal, BNode, RDF, URIRef

from taipan.mapper.properties.lov import map_table_properties
from taipan.ml.subjectcolumn.scidentifier import SCIdentifier
from taipan.agdistis import AgdistisWrapper

SCIDENTIFIER = SCIdentifier()
AGDISTIS_WRAPPER = AgdistisWrapper()

TABLE_NAMESPACE = os.environ.get("TABLE_NAMESPACE", "http://example.org/")

def get_table_meta(table, subject_column=None):
    if subject_column is None:
        subject_column = SCIDENTIFIER.identify_subject_column(table)
    if subject_column == []:
        subject_column = 0
    else:
        subject_column = subject_column[0]

    properties = map_table_properties(table)
    properties_uri = [x['uri'] if x is not None else None for x in properties]

    entities = AGDISTIS_WRAPPER.disambiguate_table(table)

    return (subject_column, properties_uri, entities)


def generate_rdf(table, subject_column=None, _format="turtle", table_class=None, skip_header=False):
    if skip_header:
        table.table = table.table[1:]
    (subject_column, properties, entities) = get_table_meta(table, subject_column=subject_column)
    g = Graph()
    for row_i, row in enumerate(table.table):
        if entities[row_i][subject_column]:
            subject_uri = entities[row_i][subject_column][0]
        else:
            subject_uri = convert_table_literal_to_uri(row[subject_column], table._id)

        subject = g.resource(subject_uri)
        if table_class:
            subject.add(URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef(table_class))

        for col_i, col in enumerate(row):
            if col_i == subject_column:
                subject.add(URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(row[subject_column]))
                continue
            if col == "":
                continue
            if properties[col_i]:
                _property = URIRef(properties[col_i])
            else:
                continue
            if col.startswith("http"):
                _obj = URIRef(col)
            else:
                _obj = Literal(col)
            subject.add(_property, _obj)

    return g.serialize(format=_format)

def convert_table_literal_to_uri(literal, table_id):
    literal = quote_plus(literal)
    uri = TABLE_NAMESPACE + "%s/%s" % (table_id, literal)
    return uri
