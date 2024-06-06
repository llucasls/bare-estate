import sys

from bare_estate.cli import main


if __name__ == "__main__":
    sys.argv[0] = "estate"
    sys.exit(main())
