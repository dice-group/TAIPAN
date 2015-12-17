# TAIPAN
Web Tables Automatic Property Mapping

## Installation
Install the project into python virtualenv and run make install:
```
   mkvirtualenv taipan
   cdvirtualenv
   mkdir src
   cd src/
   git clone https://github.com/AKSW/TAIPAN.git
   cd TAIPAN/
   make requirements
```

To run annotation application you will have to setup google and mongolab connectors with your credentials. Also, additional dependencies are required by the app (make requirements-server).

## Subject Column Identification

Simple rule based subject column identification can be run via:
```
make test-subject-column-simple-identifier
```

To run supervised subject column identification run:
```
make test-subject-column-supervised-identifier
```

See unit tests for more information.

The data for subject column gold standard is located in data/subject_column/subject_column_gold.csv

## Property Identification

To run T2K test on extended gold standard execute:
```
make test-t2k-property-mapping
```
The data retrieved from T2K is located in data/properties_t2k, we do not generate it during run. To generate the data, refer to instructions following the URI (requires at least 100 GB of RAM available): http://dws.informatik.uni-mannheim.de/en/research/T2K

The data for properties gold standard is located in data/properties_gold/dbpedia_properties (DBpedia only properties) and data/properties_gold/properties_complete (DBpedia properties + columns which potentially have connections to other ontologies).

To run TAIPAN test for property mapping execute:
```
make test-ranked-lov-property-mapping
```
