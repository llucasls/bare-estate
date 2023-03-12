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
