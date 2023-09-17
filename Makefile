PORT=3000

.PHONY: clean test run-local

run-local:
	uvicorn src.main:app --host 0.0.0.0 --port 3000 --reload

build: clean
	docker build -t users-ms --target prod .

run: build
	docker run --rm --name users-ms -p ${PORT}:3000 users-ms:latest

test:
	docker build -t users-ms-test --target test .
	- docker run --tty --name users-ms-test users-ms-test:latest
	- docker container rm -f users-ms-test
	- docker image rm -f users-ms-test
	
clean: 
	docker image rm -f users-ms 

