PYTHON = python3
PIP    = $(PYTHON) -m pip
PYTEST = $(PYTHON) -m pytest

TAR       = tar
TAR_FLAGS = --create --file=$(SRC_ARCHIVE)

SRC_FILES   = pyproject.toml README.md bare_estate/*py tests/*.py
SRC_ARCHIVE = bare_estate.tar

test: install
	$(PYTEST) --verbose --mocha

install: tar
	$(PIP) install --upgrade -r dev_requirements.txt
	$(PIP) install $(SRC_ARCHIVE)

tar:
	$(TAR) $(TAR_FLAGS) $(SRC_FILES)

.PHONY: test tar install
