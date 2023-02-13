#!/usr/bin/env python
import sys

from commands import cli_args, init, git


def main():
    status = 0

    try:
        if cli_args[0] == "init":
            status = init()
        else:
            status = git()
    except IndexError:
        print("Error: no command was provided to git", file=sys.stderr)
        status = 1

    return status


if __name__ == "__main__":
    sys.exit(main())
