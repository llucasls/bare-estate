import os
import io
import subprocess as sp
import tempfile as tmp
import sys
from sys import executable as python

import bare_estate.cli as cli


HOME = os.environ["HOME"]


def test_run_without_arguments():
    """
    Test CLI Application ::
    should print status when it doesn’t receive an argument
    """

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    cli.main(["estate"])
    result = sys.stdout.getvalue().strip().split("\n")
    sys.stdout = old_stdout

    assert result == ['']

    #raise NotImplementedError("no status command")


def test_cli_status_when_repo_doesnt_exist():
    """
    Test CLI Application ::
    should show message when repository hasn’t been initialized yet
    """

    #raise NotImplementedError("no status command")
