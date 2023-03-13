PYTHON = python
TWINE  = $(PYTHON) -m twine
PYTEST = $(PYTHON) -m pytest
VENV   = $(CURDIR)/.venv
PIP    = $(PYTHON) -m pip

PYTEST_FLAGS = -v

ifeq ($(SHELL), fish)
	ACTIVATE = source $(VENV)/bin/activate.fish
else
	ACTIVATE = . $(VENV)/bin/activate
endif

dist:
	if ! test -d dist; then \
		mkdir dist; \
	fi

build:
	$(PYTHON) -m build

check: | dist
	$(TWINE) check dist/*

publish: build
	$(TWINE) upload dist/*

clean: | dist
	rm -rf dist/*

install: $(VENV)

$(VENV): dev_requirements.txt
	if test ! -d $(VENV); then \
		$(PYTHON) -m venv $(VENV); \
	fi
	. $(VENV)/bin/activate && $(PIP) install -r dev_requirements.txt
	touch $(VENV)

test: $(VENV)
	$(ACTIVATE) && $(PYTEST) $(PYTEST_FLAGS)

coverage: $(VENV)
	$(ACTIVATE) && $(PYTEST) --cov=bare_estate/ tests/ 2> /dev/null
	if test -f .coverage; then rm .coverage; fi

.PHONY: build check publish clean install test coverage
