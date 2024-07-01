import sys
import os
import io
import tomllib

import toml


def join(*paths):
    return os.path.join(*paths).rstrip("/")


def home():
    return os.environ["HOME"]


def data_home():
    return os.environ.get("XDG_DATA_HOME", join(home(), ".local/share"))


class RepoConfigs:
    name: str
    git_dir: str
    work_tree: str

    def __init__(self, table: dict[str, str]):
        self.name = table["name"]
        if self.name == "":
            raise ValueError("repository name cannot be empty")

        self.git_dir = table.get("git_dir", self.name)
        if self.git_dir == "":
            raise ValueError("git_dir cannot be empty")

        self.work_tree = table.get("work_tree", "")

    def __str__(self):
        name = type(self).__name__
        return ('<%s name="%s" git_dir="%s" work_tree="%s">' %
                (name, self.name, self.git_dir, self.work_tree))

    @classmethod
    def from_name(cls, name: str):
        """Create a default repo config from a name."""
        table = {
            "name": name,
            "git_dir": name,
            "work_tree": "",
        }

        return cls(table)


class Configs:
    repos: dict[str, RepoConfigs]

    def __init__(self, config_file=None):
        """Read and parse a TOML configuration file."""
        if config_file is None:
            configs = self.default
        else:
            configs = self._read_toml(config_file)

        self._configs = {}

        self.base_dir = configs.get("base_dir", home())

        self.git_dir = configs.get("git_dir", join(data_home(), "bare_estate"))
        if self.git_dir == "":
            raise ValueError("git_dir cannot be empty")

        self.work_tree = configs.get("work_tree", "")

        self.repos = {
            t["name"]: RepoConfigs(t) for t in configs.get("repo", [])
        }

    def __iter__(self):
        """Yield the names of all configuration repositories."""
        for repo in self.repos.keys():
            yield repo

    @classmethod
    def from_dict(cls, config_dict):
        """Create a new Configs instance from a dictionary."""
        conf = cls()
        default = conf.default
        conf.base_dir = config_dict.get("base_dir", default["base_dir"])
        conf.git_dir = config_dict.get("git_dir", default["git_dir"])
        conf.work_tree = config_dict.get("work_tree", default["work_tree"])

        repos = config_dict.get("repo", config_dict.get("repos", {}))
        for repo_configs in repos:
            conf.create_repo(repo_configs)

        return conf

    def __str__(self):
        name = type(self).__name__
        return ('<%s base_dir="%s" git_dir="%s" work_tree="%s">' %
                (name, self.base_dir, self.git_dir, self.work_tree))

    @property
    def base_dir(self) -> str:
        """
        The directory to be used as a starting point for every git
        command. This directory will be passed as argument to the -C
        option. It is set to the user's home directory by default.
        """
        return self._configs["base_dir"]

    @base_dir.setter
    def base_dir(self, value: str):
        self._configs["base_dir"] = value

    @property
    def git_dir(self) -> str:
        """
        Set the path to a directory that contains all the configuration
        repositories.

        Each repository also has its own git_dir property, which is
        either a path relative to the general git_dir or an absolute
        one.

        By default, the general git_dir property is set to
        ${XDG_DATA_HOME}/bare_estate and each repository will be saved
        in a subdirectory which receives the repository's name.
        """
        return self._configs["git_dir"]

    @git_dir.setter
    def git_dir(self, value: str):
        self._configs["git_dir"] = value

    @property
    def work_tree(self) -> str:
        """
        Set the path to the working tree. It can be set as a path
        relative to the base directory or as an absolute path.

        Each repository can also have its own work_tree property,
        denoting a directory that contains its configuration files. In
        this case, it can either be a path relative to the general
        work_tree property or an absolute one.

        By default, each repository will have its work_tree set to the
        base directory.
        """
        return self._configs["work_tree"]

    @work_tree.setter
    def work_tree(self, value: str):
        self._configs["work_tree"] = value

    @property
    def default(self):
        return {
            "base_dir": home(),
            "git_dir": join(data_home(), "bare_estate"),
            "work_tree": "",
            "repo": [],
        }

    def get(self, name: str) -> RepoConfigs:
        """Return a config object for a particular repository."""
        if name not in self.repos:
            self.repos[name] = RepoConfigs.from_name(name)
        return self.repos[name]

    def create_repo(self, table: dict[str, str]):
        if "name" not in table:
            raise TypeError("new repository must have a name")

        self.repos[table["name"]] = RepoConfigs(table)

    def _read_toml(self, input_file):
        if isinstance(input_file, str):
            try:
                with open(input_file, mode="rb") as file:
                    return tomllib.load(file)
            except FileNotFoundError:
                return self.default
            except PermissionError:
                print(f"Warning: The file {input_file} doesn't allow reading",
                      "Using default configuration as fallback",
                      file=sys.stderr)
                return self.default
        elif not isinstance(input_file, io.IOBase):
            raise TypeError("Input must be a file path or a file-like object")
        elif not hasattr(input_file, "read"):
            raise ValueError("File must be readable")
        elif isinstance(input_file, io.BufferedIOBase):
            return tomllib.load(input_file)
        elif isinstance(input_file, io.TextIOBase):
            return toml.load(input_file)
        else:
            raise ValueError("Unsupported file-like object type")
