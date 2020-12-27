current_dir = $(shell pwd)

PROJECT = mloq
DOCKER_ORG = fragile
VERSION ?= latest
UBUNTU_NAME = $(lsb_release -s -c)
# Project usage commands

.POSIX:
style:
	black .
	isort .


.POSIX:
check:
	!(grep -R /tmp ${PROJECT}/tests)
	flakehell lint ${PROJECT}
	pylint ${PROJECT}
	black --check ${PROJECT}

.PHONY: pipenv-install
pipenv-install:
	rm -rf *.egg-info && rm -rf build && rm -rf __pycache__
	rm -f Pipfile && rm -f Pipfile.lock
	pipenv install --dev -r requirements-test.txt
	pipenv install --pre --dev -r requirements-lint.txt
	pipenv install -r requirements.txt
	pipenv install -e .
	pipenv lock

.PHONY: test
test:
	find -name "*.pyc" -delete
	pytest -s

.PHONY: pipenv-test
pipenv-test:
	find -name "*.pyc" -delete
	pipenv run pytest -s

.PHONY: docker-build
docker-build:
	docker build --pull -t ${DOCKER_ORG}/${PROJECT}:${VERSION} .

.PHONY: docker-test
docker-test:
	find -name "*.pyc" -delete
	docker run --rm -v $(pwd):/io --network host -w /${PROJECT} --entrypoint python3 ${DOCKER_ORG}/${PROJECT}:${VERSION} -m pytest

.PHONY: docker-shell
docker-shell:
	docker run --rm -v $(pwd):/io --network host -w /${PROJECT} -it ${DOCKER_ORG}/${PROJECT}:${VERSION} bash

.PHONY: docker-notebook
docker-notebook:
	docker run --rm -v $(pwd):/io --network host -w /${PROJECT} -it ${DOCKER_ORG}/${PROJECT}:${VERSION}