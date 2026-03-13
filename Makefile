# Makefile
-include .env.make   # optional local override

# Environment type: docker or local
ENV ?= docker
APP = app

ifeq ($(ENV),docker)
DC = docker-compose
RUN = $(DC) run --rm $(APP)
else
RUN =
endif

.PHONY: build up down shell django_shell wait_for_db makemigrations migrate lint test superuser start

# -----------------------------
# Docker-specific commands
# -----------------------------
build:
ifeq ($(ENV),docker)
	$(DC) build
else
	@echo "Build not needed in local mode"
endif

up:
ifeq ($(ENV),docker)
	$(DC) up
else
	cd app && python manage.py runserver
endif

down:
ifeq ($(ENV),docker)
	$(DC) down
else
	@echo "Nothing to stop"
endif

down-v:
ifeq ($(ENV),docker)
	$(DC) down -v
else
	@echo "Nothing to stop"
endif

shell:
ifeq ($(ENV),docker)
	$(RUN) sh
else
	cd app && bash
endif

# -----------------------------
# Django commands (run inside app/)
# -----------------------------
django_shell:
ifeq ($(ENV),docker)
	$(RUN) python manage.py shell_plus
else
	cd app && python manage.py shell_plus
endif

wait_for_db:
ifeq ($(ENV),docker)
	$(RUN) python manage.py wait_for_db
else
	cd app && python manage.py wait_for_db
endif

makemigrations:
ifeq ($(ENV),docker)
	$(RUN) python manage.py makemigrations
else
	cd app && python manage.py makemigrations
endif

migrate:
ifeq ($(ENV),docker)
	$(RUN) python manage.py migrate
else
	cd app && python manage.py migrate
endif

lint:
ifeq ($(ENV),docker)
	$(RUN) flake8
else
	cd app && flake8
endif

test:
ifeq ($(ENV),docker)
	$(RUN) python manage.py test
else
	cd app && python manage.py test
endif

superuser:
ifeq ($(ENV),docker)
	$(RUN) python manage.py createsuperuser
else
	cd app && python manage.py createsuperuser
endif

# -----------------------------
# Convenience command to run all
# -----------------------------
start:
	make up ENV=$(ENV)
	make wait_for_db ENV=$(ENV)
	make migrate ENV=$(ENV)
	make lint ENV=$(ENV)
	make test ENV=$(ENV)