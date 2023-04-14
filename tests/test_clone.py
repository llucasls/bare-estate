from bare_estate.commands import clone


class TestGitClone:
    "Test estate clone command"
    def test_clone_status(self, mocker):
        "should return status 0 when no error occurs"
        mock_run = mocker.patch("subprocess.run")
        mock_run().returncode = 0

        assert clone() == 0
