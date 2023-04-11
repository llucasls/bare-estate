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
	@$(MAKE) --always-make --no-print-directory $(VENV)

$(VENV): dev_requirements.txt
	if test ! -d $(VENV); then \
		$(PYTHON) -m venv $(VENV); \
	fi
	$(ACTIVATE) && $(PIP) install --upgrade -r dev_requirements.txt
	touch $(VENV)

test: $(VENV)
	-$(ACTIVATE); \
	$(BUMP) -d pyproject.toml; \
	$(BUILD) --wheel; \
	$(PIP) install --force-reinstall $$(ls -t dist/*dev* | head -1); \
	$(PYTEST) $(PYTEST_FLAGS) $(PYTEST_FILES)
	$(ACTIVATE) && $(BUMP) -D pyproject.toml
	-rm dist/*dev*

coverage: $(VENV)
	$(ACTIVATE) && $(PYTEST) --cov=$(COVERAGE_DIR) tests/ 2> /dev/null
	if test -f .coverage; then rm .coverage; fi

.PHONY: build check publish clean install test coverage

.SILENT: build check publish test coverage $(VENV)
