import subprocess as sp


ESTATE = "bare_estate/cli.py"


def test_cli_status_when_repo_doesnt_exist():
    "Test CLI Application :: should error when it doesn’t receive an argument"

    stderr = b"Error: the repository has not been initialized yet.\nYou can create a new repository using the command:\n\nbare init\n"
    result = sp.run([ESTATE, "status"], stdout=sp.PIPE, stderr=sp.PIPE)
    assert result.returncode == 2
    assert result.stderr == stderr
