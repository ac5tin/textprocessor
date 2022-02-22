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
docker-buildpush:
	docker buildx build --platform linux/amd64,linux/arm64 -t ac5tin/textprocessor . --push
podman-build:
	podman build --arch amd64 -t docker.io/ac5tin/textprocessor .
podman-push:
	podman login docker.io
	podman push docker.io/ac5tin/textprocessor