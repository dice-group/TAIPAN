import os

from taipan.pathes import TABLES_DIR
from taipan.generictable import GenericTable
from taipan.rdf.generator import generate_rdf

TEST_FILENAME = os.path.join(TABLES_DIR, "000ec48b-f25f-47ef-af12-1f897207cdb4.csv")

RDF = b'@prefix ns1: <http://dbpedia.org/ontology/> .\n@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix xml: <http://www.w3.org/XML/1998/namespace> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n<http://example.org/6db133d7-135e-5b9f-9d0f-35eda3e49890/Hilda+Akua> ns1:birthPlace <http://dbpedia.org/resource/Accra> .\n\n<http://example.org/6db133d7-135e-5b9f-9d0f-35eda3e49890/Hilde+Hefte> ns1:birthPlace <http://dbpedia.org/resource/Kristiansand> .\n\n<http://example.org/6db133d7-135e-5b9f-9d0f-35eda3e49890/Himanshi+Khurana> ns1:birthPlace <http://dbpedia.org/resource/Kiratpur_Sahib> .\n\n<http://example.org/6db133d7-135e-5b9f-9d0f-35eda3e49890/Himika+Akaneya> ns1:birthPlace <http://dbpedia.org/resource/Akita_Prefecture> .\n\n<http://example.org/6db133d7-135e-5b9f-9d0f-35eda3e49890/Hitomi+Kaji> ns1:birthPlace <http://dbpedia.org/resource/Tokyo> .\n\n<http://example.org/6db133d7-135e-5b9f-9d0f-35eda3e49890/Hossein+Mortezaeian+Abkenar> ns1:birthPlace <http://dbpedia.org/resource/Tehran> .\n\n<http://example.org/6db133d7-135e-5b9f-9d0f-35eda3e49890/Hovanes+Margarian> ns1:birthPlace <http://dbpedia.org/resource/Yerevan> .\n\n'

def test_generate_rdf():
    table = GenericTable(TEST_FILENAME)
    rdf = generate_rdf(table)
    assert rdf == RDF
