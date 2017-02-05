PLATFORM := dev
BIND := 127.0.0.1:8000
SETTINGS := DJANGO_SETTINGS_MODULE="couseit.settings.$(PLATFORM)"

.PHONY: all
all: migrations migrate fixtures

.PHONY: migrations
migrations:
	$(SETTINGS) python manage.py makemigrations account product stock

.PHONY: migrate
migrate: migrations
	$(SETTINGS) python manage.py migrate

.PHONY: fixtures
fixtures:
	$(SETTINGS) python manage.py loaddata forbiddendomains status categories properties

.PHONY: superuser
superuser:
	$(SETTINGS) python manage.py loaddata users

.PHONY: static
static:
	$(SETTINGS) python manage.py collectstatic

.PHONY: run
run: static
	$(SETTINGS) python manage.py runserver $(BIND)

.PHONY: runshell
shell:
	$(SETTINGS) python manage.py shell

.PHONY: install_deps
install_deps:
	pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf www/*
	rm db.sqlite3
