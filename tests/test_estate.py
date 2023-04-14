import os
import subprocess as sp


ESTATE = "estate"
HOME = os.environ["HOME"]


def test_run_without_arguments():
    "Test CLI Application :: should error when it doesn’t receive an argument"

    stderr = b"Error: no command was provided to git\n"
    result = sp.run([ESTATE], stdout=sp.PIPE, stderr=sp.PIPE)
    assert result.stderr == stderr
    assert result.returncode == 4

def test_cli_status_when_repo_doesnt_exist():
    """Test CLI Application ::
    should error when repository hasn’t been initialized yet"""

    env = os.environ.copy()
    env["BARE_ESTATE_LOCATION"] = f"{HOME}/dotfiles"
    stderr = b"Error: the repository has not been initialized yet.\nYou can create a new repository using the command:\n\nestate init\n"
    result = sp.run([ESTATE, "status"], stdout=sp.PIPE, stderr=sp.PIPE,
                    env=env)
    assert result.stderr == stderr
    assert result.returncode == 2
