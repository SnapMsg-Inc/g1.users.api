## users API 1.0.0
## 
PORT=3001

.PHONY: clean test run-local

help:        ## Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

run-local:   ## Run locally
	uvicorn src.main:app --host 0.0.0.0 --port ${PORT} --reload

build: clean ## Build the docker image
	docker build -t users-ms --target prod .

run: build   ## Run the docker image (and build)
	docker run --rm --name users-ms -p ${PORT}:3001 users-ms:latest

test:        ## Run dockerized tests 
	- docker compose -f docker-compose.test.yaml up --no-log-prefix --abort-on-container-exit --no-attach postgres 
	- docker compose -f docker-compose.test.yaml down
	- @docker volume rm users-ms_postgres_data > /dev/null 2>&1
	- @docker image rm -f users-ms-users_api:latest > /dev/null 2>&1

format:      ## Format (yapf must be installed)
	yapf -i --style google src/*.py test/*.py
	
clean:       ## Remove image 
	docker image rm -f users-ms

compose:  ## Stop services, remove containers, and start services again
	- docker compose -f docker-compose-local.yml down --remove-orphans 
	- docker rmi users-ms
	docker compose -f docker-compose-local.yml up --build  

