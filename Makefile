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

benchmark:
	python -m unittest discover -s ./taipan/Tests -p "*Bench.py"

benchmark-subjectcolumn:
	python -m unittest discover -s ./taipan/Tests/Benchmarking -p "SubjectColumnIdentificationBench.py"

clean-windows-characters:
	bash scripts/cleanWindowsCharacters.sh

requirements:
	pip install numpy
	pip install requests
	pip install SPARQLWrapper
