# Docker Compose alias
DC = docker-compose
APP = app

.PHONY: build up down shell wait_for_db makemigrations migrate lint test superuser start

build:
	$(DC) build

up:
	$(DC) up

down:
	$(DC) down

down-v:
	$(DC) down -v

shell:
	$(DC) run --rm $(APP) sh

django_shell:
	$(DC) run --rm $(APP) python manage.py shell_plus

wait_for_db:
	$(DC) run --rm $(APP) python manage.py wait_for_db

makemigrations:
	$(DC) run --rm $(APP) python manage.py makemigrations

migrate:
	$(DC) run --rm $(APP) python manage.py migrate

lint:
	$(DC) run --rm $(APP) flake8

test:
	$(DC) run --rm $(APP) python manage.py test

superuser:
	$(DC) run --rm $(APP) python manage.py createsuperuser

rebuild:
	$(DC) down
	$(DC) build --no-cache
	$(DC) up -d


start: up wait_for_db migrate lint test

