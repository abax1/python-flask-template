build:
	docker-compose -f docker-compose-local.yml --env-file ./.env.example build did

test:
	pytest -rf -c tests/pytest.ini --cov=src --cov-context=test --disable-warnings