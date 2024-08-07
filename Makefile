PYTHON = python3.11

VENV   = $(.CURDIR)/.venv

BUILD  = $(VENV)/bin/$(PYTHON) -m build
TWINE  = $(VENV)/bin/$(PYTHON) -m twine
PIP    = $(VENV)/bin/$(PYTHON) -m pip
PYTEST = $(VENV)/bin/$(PYTHON) -m pytest

BUMP   = $(VENV)/bin/bumpline

PYTEST_FLAGS = --verbose --mocha

COVERAGE_DIR = bare_estate/

dist:
	if test -d dist; then \
		mkdir dist; \
	fi

build: $(VENV)
	$(BUILD) $(BUILD_FLAGS)

check: dist
	$(TWINE) check dist/*

publish: build
	$(TWINE) upload dist/*

clean: dist
	rm -rf dist/*

install:
	$(MAKE) $(VENV)

$(VENV): dev_requirements.txt
	if test ! -d $(VENV); then $(PYTHON) -m venv $(VENV); fi
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r dev_requirements.txt
	touch $(VENV)

test: $(VENV)
	$(PYTEST) $(PYTEST_FLAGS) $(PYTEST_FILES)

coverage: $(VENV)
	FLAGS="--cov=$(COVERAGE_DIR)"; \
	$(MAKE) test PYTEST_FLAGS="$${FLAGS}" 2> /dev/null

.PHONY: build check publish clean install test coverage

.SILENT: dist build check publish install test coverage $(VENV)
