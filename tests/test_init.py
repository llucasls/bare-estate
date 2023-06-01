import os
import tempfile as tmp
import subprocess as sp


ESTATE = os.path.join(os.getcwd(), "estate")


class TestGitInit:
    "Test estate init command"

    def test_initialize_repository(self):
        "should create a new bare repository"

        with tmp.TemporaryDirectory(dir=os.getcwd()) as tmp_dir:

            env = os.environ.copy()
            env["BARE_ESTATE_HISTORY_LOCATION"] = os.path.join(tmp_dir,
                                                               "dotfiles")
            env["BARE_ESTATE_BASE_DIRECTORY"] = tmp_dir

            init_process = sp.run([ESTATE, "init"], env=env, stdout=sp.PIPE,
                                  stderr=sp.PIPE)

            status_process = sp.run([ESTATE, "status"], env=env,
                                    stdout=sp.PIPE, stderr=sp.PIPE)

            files = set(os.listdir(tmp_dir))

            assert init_process.returncode == 0
            assert status_process.returncode == 0
            assert files == {"dotfiles"}
