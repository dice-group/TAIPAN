dev:
	pip install -r dev-requirements.txt

requirements:
	pip install -r requirements.txt

test:
	nosetests -s tests/

data-server:
	docker run -p 80:80 osier

update-model:
	python bin/update_scident_model
