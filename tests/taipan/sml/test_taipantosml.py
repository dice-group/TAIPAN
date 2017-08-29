from taipan.sml.taipantosml import TaipanToSML

FIXTURE_MAPPING = """Prefix fn:<http://aksw.org/sparqlify/>
Prefix dbpedia-owl:<http://dbpedia.org/ontology/>
Prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#>
Prefix vivo:<http://vivoweb.org/ontology/core#>
Create View Template csvtemplate As
  Construct {
    ?subjectVariable dbpedia-owl:atRowNumber ?columnVariable1 .
    ?subjectVariable rdfs:label ?columnVariable2 .
    ?subjectVariable vivo:hasResearchArea ?columnVariable3 .
    ?subjectVariable dbpedia-owl:religion ?columnVariable4 .
  }
  With
    ?subjectVariable = uri(concat("http://example.org/table_1/", fn:urlEncode(?2)))
    ?columnVariable1 = plainLiteral(?1)
    ?columnVariable2 = plainLiteral(?2)
    ?columnVariable3 = plainLiteral(?3)
    ?columnVariable4 = plainLiteral(?4)
"""
def test_taipantosml():
    example_property_mapping = [
      {
        "col_i": 0,
        "properties": [
          {"score": 1.0, "prefixed_name": "dbpedia-owl:atRowNumber", "uri": "http://dbpedia.org/ontology/atRowNumber"},
          {"score": 0.5, "prefixed_name": "dbpedia-owl:filmNumber", "uri": "http://dbpedia.org/ontology/filmNumber"},
          {"score": 0.3, "prefixed_name": "dbpedia-owl:meshNumber", "uri": "http://dbpedia.org/ontology/meshNumber"}
        ]
      }, {
        "col_i": 1,
        "properties": [
          {"score": 1.0, "prefixed_name": "rdfs:label", "uri": "http://www.w3.org/2000/01/rdf-schema#label"}
        ]
      }, {
        "col_i": 2,
        "properties": [
          {"score": 1.0, "prefixed_name": "vivo:hasResearchArea", "uri": "http://vivoweb.org/ontology/core#hasResearchArea"},
          {"score": 0.5, "prefixed_name": "cerif:researchInterests", "uri": "http://eurocris.org/ontologies/cerif/1.3#researchInterests"},
          {"score": 0.3, "prefixed_name": "lyou:research", "uri": "http://purl.org/linkingyou/research"}
        ]
      }, {
        "col_i": 3,
        "properties": [
          {"score": 1.0, "prefixed_name": "dbpedia-owl:religion", "uri": "http://dbpedia.org/ontology/religion"},
          {"score": 0.5, "prefixed_name": "cwrc:hasReligion", "uri": "http://sparql.cwrc.ca/ontology/cwrc#hasReligion"},
          {"score": 0.3, "prefixed_name": "trait:believes", "uri": "http://contextus.net/ontology/ontomedia/ext/common/trait#believes"}
        ]
      }
    ]
    taipan_to_sml = TaipanToSML(
        example_property_mapping, "http://example.org/table_1/", 1
    )
    assert taipan_to_sml.get_mapping() == FIXTURE_MAPPING
