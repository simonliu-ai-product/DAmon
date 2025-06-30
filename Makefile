# Makefile for DataArragimon project

.PHONY: all venv install run clean

VENV_DIR = ../venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

all: run

venv:
	@echo "Checking for virtual environment..."
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV_DIR); \
		echo "Virtual environment created."; \
	else \
		echo "Virtual environment already exists."; \
	fi

install: venv
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt
	$(PIP) install build twine
	@echo "Dependencies installed."

run: install
	@echo "Running DAmon CLI..."
	$(PYTHON) DAmon/cli.py

build: clean install
	@echo "Building distribution packages..."
	$(PYTHON) -m build
	@echo "Distribution packages built in dist/."

upload: build
	@echo "Uploading to PyPI..."
	$(PYTHON) -m twine upload dist/*
	@echo "Uploaded to PyPI."

upload-test: build
	@echo "Uploading to TestPyPI..."
	$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	@echo "Uploaded to TestPyPI."

clean:
	@echo "Cleaning project..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} + 
	rm -f file.log
	rm -rf results/
	@echo "Project cleaned."

