PYTHON = python
TWINE  = $(PYTHON) -m twine
PYTEST = $(PYTHON) -m pytest
VENV   = $(CURDIR)/.venv
PIP    = $(PYTHON) -m pip

PYTEST_FLAGS = -v

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
	. $(VENV)/bin/activate && $(PYTEST) $(PYTEST_FLAGS)

.PHONY: build check publish clean install test
