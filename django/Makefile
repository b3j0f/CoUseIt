PLATFORM := dev
BIND := 127.0.0.1:8000
SETTINGS := DJANGO_SETTINGS_MODULE="couseit.settings.$(PLATFORM)"
DJANGO := $(SETTINGS) python manage.py
LOADDATA := $(DJANGO) loaddata
PYTHON := python2.7

.PHONY: all
all: migrations migrate fixtures lang

.PHONY: migrations
migrations:
	$(DJANGO) makemigrations account common

.PHONY: migrate
migrate: migrations
	$(DJANGO) migrate

.PHONY: fixtures
fixtures:
	$(LOADDATA) categories/DIY/parent
	$(LOADDATA) categories/DIY/construction_industry
	$(LOADDATA) categories/DIY/heating_air-conditionner
	$(LOADDATA) categories/DIY/hoist
	$(LOADDATA) categories/DIY/maintenance
	$(LOADDATA) categories/DIY/jardinage
	$(LOADDATA) categories/DIY/manutention
	$(LOADDATA) categories/DIY/mesure-detection
	$(LOADDATA) categories/DIY/outil
	$(LOADDATA) categories/DIY/renovation
	$(LOADDATA) categories/DIY/soudure-plomberie

	$(LOADDATA) categories/home/parent
	$(LOADDATA) categories/home/accessoire-maison
	$(LOADDATA) categories/home/electromenager
	$(LOADDATA) categories/home/materiel-medical
	$(LOADDATA) categories/home/puericulture
	$(LOADDATA) categories/home/soins-du-corps

	$(LOADDATA) categories/vehicule/parent
	$(LOADDATA) categories/vehicule/auto
	$(LOADDATA) categories/vehicule/accessoire-auto
	$(LOADDATA) categories/vehicule/moto-scooter
	$(LOADDATA) categories/vehicule/accessoire-moto
	$(LOADDATA) categories/vehicule/remorque
	$(LOADDATA) categories/vehicule/utilitaire

	$(LOADDATA) categories/holiday/parent
	$(LOADDATA) categories/holiday/appartement
	$(LOADDATA) categories/holiday/camping-car
	$(LOADDATA) categories/holiday/camping
	$(LOADDATA) categories/holiday/gite-et-chambre-d-hote
	$(LOADDATA) categories/holiday/villa

	$(LOADDATA) categories/sparetime/parent
	$(LOADDATA) categories/sparetime/bateau
	$(LOADDATA) categories/sparetime/chasse-et-peche
	$(LOADDATA) categories/sparetime/equitation
	$(LOADDATA) categories/sparetime/instrument-de-musique
	$(LOADDATA) categories/sparetime/jeu-divers
	$(LOADDATA) categories/sparetime/montagne
	$(LOADDATA) categories/sparetime/sport-d-equipe
	$(LOADDATA) categories/sparetime/sport-de-glisse
	$(LOADDATA) categories/sparetime/sport-extreme
	$(LOADDATA) categories/sparetime/sport-individuel
	$(LOADDATA) categories/sparetime/velo

	$(LOADDATA) categories/high-tech/parent
	$(LOADDATA) categories/high-tech/console-de-jeu
	$(LOADDATA) categories/high-tech/GPS
	$(LOADDATA) categories/high-tech/informatique
	$(LOADDATA) categories/high-tech/materiel-audio
	$(LOADDATA) categories/high-tech/materiel-video
	$(LOADDATA) categories/high-tech/photo
	$(LOADDATA) categories/high-tech/telephone-et-PDA

	$(LOADDATA) categories/event/parent
	$(LOADDATA) categories/event/animation
	$(LOADDATA) categories/event/cuisine
	$(LOADDATA) categories/event/mobilier
	$(LOADDATA) categories/event/reception
	$(LOADDATA) categories/event/salle
	$(LOADDATA) categories/event/securite
	$(LOADDATA) categories/event/sono-et-eclairage
	$(LOADDATA) categories/event/vetement-de-soiree

	$(LOADDATA) categories/stock/parent
	$(LOADDATA) categories/stock/compartment
	$(LOADDATA) categories/stock/transport

	$(LOADDATA) status
	$(LOADDATA) properties

.PHONY: superuser
superuser:
	$(LOADDATA) users forbiddendomains

.PHONY: static
static:
	$(DJANGO) collectstatic

.PHONY: run
run: static
	$(DJANGO) runserver $(BIND)

.PHONY: runshell
shell:
	$(DJANGO) shell

.PHONY: install_deps
install_deps:
	pip install -r requirements/$(PLATFORM).txt

.PHONY: venv
venv:
	virtualenv venv -p $(PYTHON)
	source venv/bin/activate

.PHONY: graph_models # require dev environment
graph_models:
	$(DJANGO) graph_models -a > graph_models.dot
	$(DJANGO) graph_models -a -g -o graph_models.png

.PHONY: clean
clean:
	rm -rf www/*

.PHONY: clean-hard
clean-hard: clean
	rm -rf */migrations/0* ; $(DJANGO) dumpdata > dumped ; $(DJANGO) flush ; rm -rf db.sqlite3 ; rm -rf venv

.PHONY: update
update: clean-hard all

.PHONY: lang
lang:
	$(DJANGO) makemessages
	$(DJANGO) compilemessages