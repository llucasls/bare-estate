import sys
import subprocess as sp
import tempfile as tmp

import toml


BUMP = "tasks/bump.py"


def test_error_when_no_arguments_are_given():
    result = sp.run([BUMP], stdout=sp.PIPE, stderr=sp.PIPE)

    assert result.returncode == 2


def test_dont_change_version_when_release_isnt_given():
    with tmp.NamedTemporaryFile() as tmp_file:
        with open(tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.5"\n')

        result = sp.run([BUMP, tmp_file.name])
        version = toml.load(tmp_file.name)["project"]["version"]

        assert version == "1.5"


class TestIncreaseMajor:
    tmp_file = tmp.NamedTemporaryFile()

    def test_with_major(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1"\n')

        result = sp.run([BUMP, self.tmp_file.name, "major"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "2"

    def test_with_minor(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.5"\n')

        result = sp.run([BUMP, self.tmp_file.name, "major"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "2.0"

    def test_with_micro(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.5.2"\n')

        result = sp.run([BUMP, self.tmp_file.name, "major"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "2.0.0"

    def test_with_major_alpha(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--alpha", "major"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "2a"

    def test_with_major_beta(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--beta", "major"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "2b"

    def test_with_major_rc(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--rc", "major"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "2rc"

    def test_with_minor_alpha(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--alpha", "minor"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "2.0a"

    def test_with_minor_beta(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--beta", "minor"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "2.0b"

    def test_with_minor_rc(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--rc", "minor"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "2.0rc"

    def test_with_micro_alpha(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4.9"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--alpha", "micro"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "2.0.0a"

    def test_with_micro_beta(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4.9"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--beta", "micro"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "2.0.0b"

    def test_with_micro_rc(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4.9"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--rc", "micro"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "2.0.0rc"


class TestIncreaseMinor:
    tmp_file = tmp.NamedTemporaryFile()

    def test_with_major(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1"\n')

        result = sp.run([BUMP, self.tmp_file.name, "minor"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.1"

    def test_with_minor(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.5"\n')

        result = sp.run([BUMP, self.tmp_file.name, "minor"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.6"

    def test_with_micro(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.5.2"\n')

        result = sp.run([BUMP, self.tmp_file.name, "minor"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.6.0"

    def test_with_major_alpha(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--alpha", "major"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.1a"

    def test_with_major_beta(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--beta", "major"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.1b"

    def test_with_major_rc(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--rc", "major"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.1rc"

    def test_with_minor_alpha(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--alpha", "minor"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.5a"

    def test_with_minor_beta(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--beta", "minor"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.5b"

    def test_with_minor_rc(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--rc", "minor"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.5rc"

    def test_with_micro_alpha(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4.9"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--alpha", "micro"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.5.0a"

    def test_with_micro_beta(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4.9"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--beta", "micro"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.5.0b"

    def test_with_micro_rc(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4.9"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--rc", "micro"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.5.0rc"


class TestIncreaseMicro:
    tmp_file = tmp.NamedTemporaryFile()

    def test_with_major(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1"\n')

        result = sp.run([BUMP, self.tmp_file.name, "micro"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.0.1"

    def test_with_minor(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.5"\n')

        result = sp.run([BUMP, self.tmp_file.name, "micro"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.5.1"

    def test_with_micro(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.5.2"\n')

        result = sp.run([BUMP, self.tmp_file.name, "micro"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.5.3"

    def test_with_major_alpha(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--alpha", "major"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.0.1a"

    def test_with_major_beta(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--beta", "major"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.0.1b"

    def test_with_major_rc(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--rc", "major"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.0.1rc"

    def test_with_minor_alpha(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--alpha", "minor"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.4.1a"

    def test_with_minor_beta(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--beta", "minor"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.4.1b"

    def test_with_minor_rc(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--rc", "minor"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.4.1rc"

    def test_with_micro_alpha(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4.9"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--alpha", "micro"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.4.10a"

    def test_with_micro_beta(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4.9"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--beta", "micro"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.4.10b"

    def test_with_micro_rc(self):
        with open(self.tmp_file.name, "w") as file:
            file.write('[project]\nversion = "1.4.9"\n')

        result = sp.run([BUMP, self.tmp_file.name, "--rc", "micro"])
        version = toml.load(self.tmp_file.name)["project"]["version"]

        assert version == "1.4.10rc"
