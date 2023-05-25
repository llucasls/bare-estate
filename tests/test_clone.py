import os
import tempfile as tmp
import subprocess as sp
import tarfile

from bare_estate.commands import clone


ESTATE = os.path.join(os.getcwd(), "estate")
HOME = os.environ["HOME"]
TARBALL_PATH = "tests/mocks/dotfiles.tar.gz"


class TestGitClone:
    "Test estate clone command"
    def test_clone_status(self, mocker):
        "should return status 0 when no error occurs"

        mock_run = mocker.patch("subprocess.run")
        mock_run().returncode = 0

        assert clone() == 0

    def test_clone_repository(self):
        "should create a bare repository with the same files from a remote repo"

        with tmp.TemporaryDirectory(dir=os.getcwd()) as tmp_dir:
            with tarfile.open(TARBALL_PATH, mode="r:gz") as tar:
                tar.extractall(path=tmp_dir)

            dotfiles_repo = os.path.join(tmp_dir, "dotfiles_repo")

            env = os.environ.copy()
            env["BARE_ESTATE_LOCATION"] = os.path.join(tmp_dir, "dotfiles")

            proc = sp.run([ESTATE, "clone", dotfiles_repo], env=env,
                          stdout=sp.PIPE, stderr=sp.PIPE)

            files = set(os.listdir(tmp_dir))

            assert proc.returncode == 0
            assert files == {"dotfiles", "dotfiles_repo", ".profile"}
