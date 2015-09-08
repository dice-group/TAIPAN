default:
	echo "no default target for this make file"
	echo "to run test: make test"

install:
	cp taipan/Config/ExternalUris.py-sample taipan/Config/ExternalUris.py

test:
	python -m unittest discover -s ./taipan/Tests -p "*Test.py"

benchmark:
	python -m unittest discover -s ./taipan/Tests -p "*Bench.py"
