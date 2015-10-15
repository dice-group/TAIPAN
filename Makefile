default:
	echo "no default target for this make file"
	echo "to run test: make test"

install: requirements
	cp taipan/Config/ExternalUris.py-sample taipan/Config/ExternalUris.py
	mkdir results
	mkdir cache

test:
	python -m unittest discover -s ./taipan/Tests -p "*Test.py"

test-t2d-sampler:
	python -m unittest discover -s ./taipan/Tests/T2D -p "SamplerTest.py"

test-property-mapping:
	python -m unittest discover -s ./taipan/Tests/Learning/PropertyMapping -p "PropertyMappingTest.py"

benchmark:
	python -m unittest discover -s ./taipan/Tests -p "*Bench.py"

benchmark-subject-column-identification:
	python -m unittest discover -s ./taipan/Tests/Benchmarking -p "SubjectColumnIdentificationBench.py"

benchmark-simple-property-mapping:
	python -m unittest discover -s ./taipan/Tests/Benchmarking -p "PropertyMappingBench.py"

clean-windows-characters:
	bash scripts/cleanWindowsCharacters.sh

requirements:
	pip install numpy
	pip install requests
	pip install SPARQLWrapper
