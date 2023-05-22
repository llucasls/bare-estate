import os

from bare_estate.commands import clone


ESTATE = os.path.join(os.getcwd(), "estate")
HOME = os.environ["HOME"]


class TestGitClone:
    "Test estate clone command"
    def test_clone_status(self, mocker):
        "should return status 0 when no error occurs"

        mock_run = mocker.patch("subprocess.run")
        mock_run().returncode = 0

        assert clone() == 0

    def test_clone_repository(self):
        "should create a bare repository with the same files from a remote repo"

        env = os.environ.copy()
        #env["BARE_ESTATE_LOCATION"] = tmp_dir

        raise NotImplementedError("test clone command")
