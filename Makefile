
.PHONY: clean

run: clean 
	docker compose up

clean: 
	docker compose down
	docker image rm -f users-ms
	docker container rm -f users-ms
