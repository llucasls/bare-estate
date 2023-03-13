PYTHON = python
TWINE = $(PYTHON) -m twine
PYTEST = $(PYTHON) -m pytest
VENV = $(CURDIR)/.venv

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

$(VENV):
	$(PYTHON) -m $(VENV)

test:
	$(PYTEST)

.PHONY: build check publish clean test
