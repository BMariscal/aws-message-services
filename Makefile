PYTHON = python3

run:
	docker-compose up

rebuild:
	docker-compose up -d --build --force-recreate
	docker-compose up

teardown:
	docker-compose down
	docker system prune
