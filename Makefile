prepare:
	pip install -r requirements.txt
	python -m spacy download zh_core_web_lg
	python -m spacy download en_core_web_lg

test: 
	python -m unittest -v tests/*.py

run:
	python app.py

lint:
	pylint *.py **/*.py

docker-build:
	docker build -t textprocessor .