#!/usr/bin/env python
import sys
import subprocess as sp

from config import configs


cli_args = sys.argv[1:]


def init():
    proc = sp.Popen(["git", *cli_args])
    proc.communicate()
    return proc.returncode


def git():
    proc = sp.Popen(["git", *cli_args])
    proc.communicate()
    return proc.returncode


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
