# Atajos para Linux / Mac. En Windows usa directamente: python run.py
PYTHON ?= python3

.PHONY: all instalar test rapido ejemplo limpiar

all: instalar          ## Instala dependencias, pasa los tests y lanza los experimentos
	$(PYTHON) run.py

instalar:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) run.py --tests

rapido:
	$(PYTHON) run.py --rapido

ejemplo:
	$(PYTHON) run.py --ejemplo

limpiar:
	rm -rf resultados datos __pycache__ */__pycache__
