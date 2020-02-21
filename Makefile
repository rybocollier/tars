default: deps 

.PHONY: deps
deps:
	docker-compose run --no-deps --rm --entrypoint="pip-compile --generate-hashes --output-file requirements/requirements.txt requirements/requirements.in" tars

.PHONY: build
build:
	docker-compose build

.PHONY: run
run:
	./scripts/run.sh

.PHONY: stop
stop:
	./scripts/stop.sh

#.PHONY: dist
#dist:
#	docker build -t build_api:latest -f Dockerfile.local .