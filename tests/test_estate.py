import os
import subprocess as sp
import tempfile as tmp
from sys import executable as python


ESTATE = os.path.join(os.getcwd(), "estate")
HOME = os.environ["HOME"]


def test_run_without_arguments():
    "Test CLI Application :: should error when it doesn’t receive an argument"

    stderr = b"Error: no command was provided to git\n"
    result = sp.run([python, ESTATE], stdout=sp.PIPE, stderr=sp.PIPE)
    assert result.stderr == stderr
    assert result.returncode == 4

def test_cli_status_when_repo_doesnt_exist():
    """Test CLI Application ::
    should error when repository hasn’t been initialized yet"""

    tmp_dir = tmp.NamedTemporaryFile(delete=True, dir=HOME).name
    env = os.environ.copy()
    env["BARE_ESTATE_HISTORY_LOCATION"] = tmp_dir

    stderr = b"Error: the repository has not been initialized yet.\nYou can create a new repository using the command:\n\nestate init\n"
    result = sp.run([python, ESTATE, "status"], stdout=sp.PIPE, stderr=sp.PIPE,
                    env=env)
    assert result.stderr == stderr
    assert result.returncode == 2
