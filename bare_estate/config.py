import sys
import os
import io
import tomllib
import typing as t

import toml


def join(*paths: str) -> str:
    return os.path.join(*paths).rstrip("/")


def home():
    return os.environ["HOME"]


def data_home():
    return os.environ.get("XDG_DATA_HOME", join(home(), ".local/share"))


def config_home():
    return os.environ.get("XDG_CONFIG_HOME", join(home(), ".config"))


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
    def from_name(cls, name: str, git_dir: str, work_tree: str):
        """Create a default repo config from a name."""
        table = {
            "name": name,
            "git_dir": join(git_dir, name),
            "work_tree": join(work_tree, ""),
        }

        return cls(table)


class Configs:
    repos: dict[str, RepoConfigs]
    filename: str

    def __init__(self, config_file=None):
        """Read and parse a TOML configuration file."""
        if config_file is None:
            self.filename = join(config_home(), "bare_estate.toml")
            try:
                with open(self.filename) as file:
                    configs = self._read_toml(file)
            except (FileNotFoundError, PermissionError):
                configs = self.default
        elif isinstance(config_file, str):
            configs = self._read_toml(config_file)
            self.filename = config_file
        else:
            configs = self._read_toml(config_file)
            self.filename = join(config_home(), "bare_estate.toml")

        self._configs = {}
        gen_configs = configs.get("config", {})

        self.base_dir = gen_configs.get("base_dir", home())

        self.git_dir = gen_configs.get(
            "git_dir", join(data_home(), "bare_estate")
        )
        if self.git_dir == "":
            raise ValueError("git_dir cannot be empty")

        self.work_tree = gen_configs.get("work_tree", "")

        self.repos = {}

        for table in configs.get("repo", []):
            if "name" not in table:
                raise TypeError("new repository must have a name")

            repo_config = {
                "name": table["name"],
                "git_dir": table.get("git_dir", table["name"]),
                "work_tree": table.get("work_tree", ""),
            }
            self.repos[table["name"]] = RepoConfigs(repo_config)

    @classmethod
    def from_dict(cls, config_dict: dict[str, t.Any]):
        """Create a new Configs instance from a dictionary."""
        conf = cls()
        default = conf.default
        gen_configs = config_dict.get("config", {})
        conf.base_dir = gen_configs.get("base_dir", default["base_dir"])
        conf.git_dir = gen_configs.get("git_dir", default["git_dir"])
        conf.work_tree = gen_configs.get("work_tree", default["work_tree"])

        repos = config_dict.get("repo", config_dict.get("repos", {}))
        for repo_configs in repos:
            if "name" not in repo_configs:
                raise TypeError("new repository must have a name")

            name = repo_configs["name"]
            repo_configs["git_dir"] = repo_configs.get("git_dir", name)
            repo_configs["work_tree"] = repo_configs.get("work_tree", "")

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

    def get(self, name: str, key=None) -> RepoConfigs | str | None:
        if name not in self.repos:
            return None
        elif key is None:
            return self.repos[name]

        return join(getattr(self, key, ""), getattr(self.repos[name], key))

    def dump(self, file: io.TextIOBase):
        """Write TOML configuration into a file-like object."""
        repos = []

        for r in self.repos.values():
            repo: dict[str, str] = {"name": r.name}
            if r.git_dir != r.name:
                repo["git_dir"] = r.git_dir
            if r.work_tree != "":
                repo["work_tree"] = r.work_tree
            repos.append(repo)

        c: dict[str, t.Any] = {"config": {"base_dir": self.base_dir}}
        if self.git_dir != self.default["git_dir"]:
            c["config"]["git_dir"] = self.git_dir
        if self.work_tree != self.default["work_tree"]:
            c["config"]["work_tree"] = self.work_tree

        toml.dump(c, file)
        file.write("\n")

        if len(repos) > 0:
            file.write(toml.dumps({"repo": repos}).strip())
            file.write("\n")

    def create_repo(self, table: dict[str, str]):
        if "name" not in table:
            raise TypeError("new repository must have a name")

        self.repos[table["name"]] = RepoConfigs(table)

    def create_config_file(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, mode="x") as file:
            self.dump(file)

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
                      sep="\n",
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
