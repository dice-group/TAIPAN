# taipan-library

# Installation Instructions
```bash
$ mkvirtualenv -p $(which python3) taipan
$ cdvirtualenv
$ mkdir src && cd src
$ git clone git@github.com:dice-group/TAIPAN.git && cd TAIPAN
$ pip install -e .
```

# To Install Dev Requirements (nose, ipdb)
```
make dev
```

# Usage
For subject column identification use scidentifier script, for example:
```
$ ./bin/scidentifier data/tables/329f559f-981f-4e7a-af8c-df8838caf74a.csv
[0]
```
For property recommendation use propertyrecommender script, for example:
```
$ ./bin/propertyrecommender data/tables/329f559f-981f-4e7a-af8c-df8838caf74a.csv
[
    {
        "col_i": 0,
        "properties": [
            {
                "score": 2.039461,
                "prefixed_name": "dbpedia-owl:recordLabel",
                "uri": "http://dbpedia.org/ontology/recordLabel"
            },
            {
                "score": 1.4604475,
                "prefixed_name": "dbpedia-owl:distributingLabel",
                "uri": "http://dbpedia.org/ontology/distributingLabel"
            },
            ... (trimmed)
        ]
    }
]
```
For SML mapping generation:
```
$ ./bin/smlmapping data/tables/329f559f-981f-4e7a-af8c-df8838caf74a.csv http://example.org
Prefix fn:<http://aksw.org/sparqlify/>
Prefix dbpedia-owl:<http://dbpedia.org/ontology/>
Create View Template csvtemplate As
  Construct {
    ?subjectVariable dbpedia-owl:recordLabel ?columnVariable1 .
  }
  With
    ?subjectVariable = uri(concat("http://example.org", fn:urlEncode(?1)))
    ?columnVariable1 = plainLiteral(?1)
```
You can use mappings together with SPARQLify to convert csv to RDF:
```
$ ./bin/smlmapping data/tables/329f559f-981f-4e7a-af8c-df8838caf74a.csv http://example.org > generated_mapping.sml
$ sparqlify-csv -c generated_mapping.sml -f data/tables/329f559f-981f-4e7a-af8c-df8838caf74a.csv
```
