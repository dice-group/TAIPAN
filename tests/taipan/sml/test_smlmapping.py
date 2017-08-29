from taipan.sml.smlmapping import SMLMapping

FIXTURE_MAPPING = """Prefix fn:<http://aksw.org/sparqlify/>
Prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#>
Prefix vivo:<http://vivoweb.org/ontology/core#>
Prefix xsd:<http://www.w3.org/2001/XMLSchema#>
Prefix dbo:<http://dbpedia.org/ontology/>
Create View Template csvtemplate As
  Construct {
    ?scientistUri rdfs:label ?scientistLabel .
    ?scientistUri vivo:hasResearchArea ?researchLabel .
    ?scientistUri dbo:religion ?religionLabel .
  }
  With
    ?scientistUri = uri(concat("http://example.org/resource/scientist/", fn:urlEncode(?2)))
    ?scientistLabel = plainLiteral(?2)
    ?researchLabel = plainLiteral(?3)
    ?religionLabel = plainLiteral(?4)
"""
def test_smlmapping():
    mapping = SMLMapping()
    mapping.add_prefix("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
    mapping.add_prefix("vivo", "http://vivoweb.org/ontology/core#")
    mapping.add_prefix("xsd", "http://www.w3.org/2001/XMLSchema#")
    mapping.add_prefix("dbo", "http://dbpedia.org/ontology/")

    mapping.add_variable_binding("scientistUri", "uri(concat(\"http://example.org/resource/scientist/\", fn:urlEncode(?2)))")
    mapping.add_variable_binding("scientistLabel", "plainLiteral(?2)")
    mapping.add_variable_binding("researchLabel", "plainLiteral(?3)")
    mapping.add_variable_binding("religionLabel", "plainLiteral(?4)")

    mapping.add_triple_binding("scientistUri", "rdfs:label", "scientistLabel")
    mapping.add_triple_binding("scientistUri", "vivo:hasResearchArea", "researchLabel")
    mapping.add_triple_binding("scientistUri", "dbo:religion", "religionLabel")

    assert mapping.get_mapping() == FIXTURE_MAPPING
