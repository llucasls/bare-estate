PYTHON = python3
BUILD  = /usr/bin/python3 -m build
TWINE  = $(PYTHON) -m twine
PYTEST = $(PYTHON) -m pytest
PIP    = $(PYTHON) -m pip

VENV     = $(CURDIR)/.venv
ACTIVATE = . $(VENV)/bin/activate

BUMP = bumpline

PYTEST_FLAGS = --verbose --mocha

COVERAGE_DIR = bare_estate/

TAR       = tar
TAR_FLAGS = --create --file=$(SRC_ARCHIVE)

SRC_FILES   = pyproject.toml README.md bare_estate/*.py tests/*.py
SRC_ARCHIVE = bare_estate.tar

dist:
	mkdir dist

build:
	$(BUILD) $(BUILD_FLAGS)

check: | dist
	$(TWINE) check dist/*

publish: build
	$(TWINE) upload dist/*

clean: | dist
	rm -rf dist/*

install:
	$(MAKE) --always-make --no-print-directory $(VENV)

$(VENV): dev_requirements.txt
	if test ! -d $(VENV); then \
		$(PYTHON) -m venv $(VENV); \
	fi
	$(ACTIVATE) && $(PIP) install --upgrade -r dev_requirements.txt
	touch $(VENV)

test: $(VENV)
	$(TAR) $(TAR_FLAGS) $(SRC_FILES)
	-$(ACTIVATE); $(PIP) install $(SRC_ARCHIVE); \
	$(PYTEST) $(PYTEST_FLAGS) $(PYTEST_FILES); \
	$(PIP) uninstall bare-estate --yes &> /dev/null
	-rm $(SRC_ARCHIVE)

coverage: $(VENV)
	$(ACTIVATE) && $(PYTEST) --cov=$(COVERAGE_DIR) tests/ 2> /dev/null
	if test -f .coverage; then rm .coverage; fi

.PHONY: build check publish clean install test coverage

.SILENT: build check publish install test coverage $(VENV)
