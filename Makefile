default:
	echo "no default target for this make file"
	echo "to run test: make test"

test:
	python -m unittest discover -s ./taipan/Tests -p "*Test.py"
