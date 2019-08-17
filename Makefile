run: service
	docker-compose build
	docker-compose up

test: test-acceptance

test-acceptance: tests/acceptance
	mongoimport --host localhost --port 5000 \
		--db team --collection workers --drop \
		--file tests/data/workers.json --jsonArray
	pytest tests/acceptance -v
