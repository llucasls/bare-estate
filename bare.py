#!/usr/bin/env python
import sys

from commands import cli_args, log_err, init, git


def main():
    status = 0

    try:
        if cli_args[0] == "init":
            status = init()
        else:
            status = git()

    except FileNotFoundError:
        log_err("Error: the repository has not been initialized yet.")
        log_err("You can create a new repository using the command:\n")
        log_err("bare init")
        status = 2

    except TypeError:
        log_err("Error: the directory found is not a git repository.")
        status = 3

    except NotADirectoryError as error:
        file = error.filename
        log_err(f"Error: A file with the name {file} already exists.")
        status = 3

    except IndexError:
        log_err("Error: no command was provided to git")
        status = 4

    return status


if __name__ == "__main__":
    sys.exit(main())
