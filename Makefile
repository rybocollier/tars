default: deps 

.PHONY: deps
deps:
	docker-compose run --no-deps --rm --entrypoint="pip-compile --generate-hashes --output-file requirements/requirements.txt requirements/requirements.in" tars

.PHONY: build
build:
	docker-compose build

.PHONY: run
run:
	docker-compose up

.PHONY: stop
stop:
	docker-compose stop
	docker-compose down --volumes --remove-orphans --rmi all

#.PHONY: dist
#dist:
#	docker build -t build_api:latest -f Dockerfile.local .