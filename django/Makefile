PLATFORM := dev
BIND := 127.0.0.1:8000
SETTINGS := DJANGO_SETTINGS_MODULE="couseit.settings.$(PLATFORM)"
DJANGO := $(SETTINGS) python manage.py
LOADDATA := $(DJANGO) loaddata
PYTHON := python2.7

.PHONY: all
all: migrations migrate fixtures

.PHONY: migrations
migrations:
	$(DJANGO) makemigrations account product

.PHONY: migrate
migrate: migrations
	$(DJANGO) migrate

.PHONY: fixtures
fixtures:
	$(LOADDATA) categories/bricolage/parent
	$(LOADDATA) categories/bricolage/btp
	$(LOADDATA) categories/bricolage/chauffage-climatiseur
	$(LOADDATA) categories/bricolage/elevation
	$(LOADDATA) categories/bricolage/entretien
	$(LOADDATA) categories/bricolage/jardinage
	$(LOADDATA) categories/bricolage/manutention
	$(LOADDATA) categories/bricolage/mesure-detection
	$(LOADDATA) categories/bricolage/outil
	$(LOADDATA) categories/bricolage/renovation
	$(LOADDATA) categories/bricolage/soudure-plomberie

	$(LOADDATA) categories/maison/parent
	$(LOADDATA) categories/maison/accessoire-maison
	$(LOADDATA) categories/maison/electromenager
	$(LOADDATA) categories/maison/materiel-medical
	$(LOADDATA) categories/maison/puericulture
	$(LOADDATA) categories/maison/soins-du-corps

	$(LOADDATA) categories/vehicule/parent
	$(LOADDATA) categories/vehicule/auto
	$(LOADDATA) categories/vehicule/accessoire-auto
	$(LOADDATA) categories/vehicule/moto-scooter
	$(LOADDATA) categories/vehicule/accessoire-moto
	$(LOADDATA) categories/vehicule/remorque
	$(LOADDATA) categories/vehicule/utilitaire

	$(LOADDATA) categories/vacance/parent
	$(LOADDATA) categories/vacance/appartement
	$(LOADDATA) categories/vacance/camping-car
	$(LOADDATA) categories/vacance/camping
	$(LOADDATA) categories/vacance/gite-et-chambre-d-hote
	$(LOADDATA) categories/vacance/villa

	$(LOADDATA) categories/loisir/parent
	$(LOADDATA) categories/loisir/bateau
	$(LOADDATA) categories/loisir/chasse-et-peche
	$(LOADDATA) categories/loisir/equitation
	$(LOADDATA) categories/loisir/instrument-de-musique
	$(LOADDATA) categories/loisir/jeu-divers
	$(LOADDATA) categories/loisir/montagne
	$(LOADDATA) categories/loisir/sport-d-equipe
	$(LOADDATA) categories/loisir/sport-de-glisse
	$(LOADDATA) categories/loisir/sport-extreme
	$(LOADDATA) categories/loisir/sport-individuel
	$(LOADDATA) categories/loisir/velo

	$(LOADDATA) categories/high-tech/parent
	$(LOADDATA) categories/high-tech/console-de-jeu
	$(LOADDATA) categories/high-tech/GPS
	$(LOADDATA) categories/high-tech/informatique
	$(LOADDATA) categories/high-tech/materiel-audio
	$(LOADDATA) categories/high-tech/materiel-video
	$(LOADDATA) categories/high-tech/photo
	$(LOADDATA) categories/high-tech/telephone-et-PDA

	$(LOADDATA) categories/evenement/parent
	$(LOADDATA) categories/evenement/animation
	$(LOADDATA) categories/evenement/cuisine
	$(LOADDATA) categories/evenement/mobilier
	$(LOADDATA) categories/evenement/reception
	$(LOADDATA) categories/evenement/salle
	$(LOADDATA) categories/evenement/securite
	$(LOADDATA) categories/evenement/sono-et-eclairage
	$(LOADDATA) categories/evenement/vetement-de-soiree

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
