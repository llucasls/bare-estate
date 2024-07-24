import os
import subprocess as sp
import shutil
import re
import typing as t
import getopt

from bare_estate.config import Configs


whitespace = re.compile(r"\s")

ArgV: t.TypeAlias = list[str]
ParsedArgs: t.TypeAlias = tuple[dict[str, t.Any], ArgV]


class Action(t.Protocol):
    def __call__(self, argv: list[str], env=os.environ, **options):
        pass


def _format_shell_arg(arg: str):
    if len(arg) == 0:
        return "''"

    match = whitespace.search(arg)
    space_index = match.start() if match else -1
    eq_index = arg.find("=")

    if match is None:
        return arg
    elif eq_index == -1:
        return f"'{arg}'"
    elif eq_index > 0 and eq_index < space_index:
        return f"{arg[:eq_index+1]}'{arg[eq_index+1:]}'"

    return f"'{arg}'"


class ArgParser:
    """Parse operators and flags from a list of command-line arguments."""

    @staticmethod
    def init(argv: ArgV) -> ParsedArgs:
        short_opts = "d:u:"
        long_opts = ["git-dir=", "url="]

        options: dict[str, t.Any] = {}
        opts, args = getopt.getopt(argv[1:], short_opts, long_opts)

        for flag, value in opts:
            if flag in ("-d", "--git-dir"):
                options["git_dir"] = value
            elif flag in ("-u", "--url"):
                options["url"] = value

        return options, args

    @staticmethod
    def clone(argv: ArgV) -> ParsedArgs:
        short_opts = "r:d:"
        long_opts = ["repo=", "git-dir="]

        options: dict[str, t.Any] = {}
        opts, args = getopt.getopt(argv[1:], short_opts, long_opts)

        for flag, value in opts:
            if flag in ("-r", "--repo"):
                options["name"] = value
            elif flag in ("-d", "--git-dir"):
                options["git_dir"] = value

        return options, args


class Command:
    """
    A helper class to execute git commands.

    It exposes two main methods in 'run' and 'dry_run'. They both
    receive a callback and the parameters to be passed into it. The
    'run' method will execute the command using the input callback
    while 'dry_run' just prints which commands would be executed,
    as one or more shell commands.

    The callback methods implement commands that you would use in a
    normal git project, such as 'init' and 'clone', or you can also use
    the general case function labeled as 'git'. Each of those also
    receive a callback, called action, that receives a list of strings
    representing a git command. The action callback is subprocess.run if
    the calling method is 'run' and self.parse_shell_cmd if it is
    'dry_run'. That way you can either execute the commands as
    subprocesses or print them to stdout as shell commands.
    """
    configs: Configs

    def __init__(self, configs: Configs):
        """Read configuration options from a Configs object."""
        self.configs = configs

    def run(self, comm, *args, **kwargs) -> int:
        """Execute an estate command."""
        caller = getattr(self, comm) if isinstance(comm, str) else comm

        for process in caller(sp.run, *args, **kwargs):
            if process.returncode != 0:
                return process.returncode

        return 0

    def dry_run(self, comm, argv: ArgV, **kwargs):
        """Print shell commands without executing."""
        try:
            caller = getattr(self, comm) if isinstance(comm, str) else comm
        except AttributeError as err:
            caller = self.git

        for cmd in caller(self.parse_shell_cmd, argv, **kwargs):
            print(*cmd)

    @staticmethod
    def parse_shell_cmd(arg_list: list[str], env=os.environ) -> list[str]:
        """
        Returns a list of arguments as a representation of a proper shell
        command. This will add quotation marks around arguments with any
        whitespace characters in them.
        """

        command = []
        env_list = ["GIT_DIR", "GIT_WORK_TREE"]

        for var in env_list:
            if var in env:
                command.append(f"{var}={_format_shell_arg(env[var])}")

        for arg in arg_list:
            command.append(_format_shell_arg(arg))

        return command

    def init(self, action: Action, argv: ArgV, env=os.environ):
        """Initialize a new git repository."""

        if shutil.which("git") is None:
            raise FileNotFoundError(5, "Command not found", "git")

        options, operators = ArgParser.init(argv)

        name = operators[0]
        configs = self.configs
        base_dir = configs.base_dir

        git_dir = options.get("git_dir", name)
        work_tree = operators[1] if len(operators) > 1 else ""

        configs.create_repo({
            "name": name,
            "git_dir": git_dir,
            "work_tree": work_tree,
        })

        if work_tree == "":
            git_cmd = list(self._generate(name, work_tree=None))
            yield action([*git_cmd, "init"], env=env)
            yield action([*git_cmd, "config", "core.bare", "false"], env=env)
            repo_work_tree = ""
        else:
            git_cmd = list(self._generate(
                name, git_dir=None, work_tree=None
            ))
            repo_git_dir = configs.get(name, "git_dir")
            repo_work_tree = str(configs.get(name, "work_tree"))

            yield action([
                *git_cmd, "init",
                f"--separate-git-dir={repo_git_dir}",
                repo_work_tree
            ], env=env)

        work_tree_path = os.path.join(configs.base_dir, repo_work_tree)
        if os.path.abspath(work_tree_path) == env.get("HOME"):
            show = "no"
        else:
            show = "all"
        git_cmd = list(self._generate(name, work_tree=None))
        yield action([*git_cmd, "config", "status.showUntrackedFiles", show],
                     env=env)

    def clone(self, action: Action, argv: ArgV, env=os.environ):
        if shutil.which("git") is None:
            raise FileNotFoundError(5, "Command not found", "git")

        if len(argv) < 2:
            raise RuntimeError("too few arguments")

        options, operators = ArgParser.clone(argv)

        url = operators[0]
        work_tree = operators[1] if len(operators) > 1 else None
        name = options.get("name", os.path.basename(url).rstrip(".git"))
        git_dir = options.get("git_dir", name)

        table = {"name": name, "git_dir": git_dir}
        if work_tree is not None:
            table["work_tree"] = work_tree

        configs = self.configs
        configs.create_repo(table)

        git_cmd = list(self._generate(name, work_tree=None, git_dir=None))
        git_dir = f"--separate-git-dir={os.path.join(configs.git_dir, name)}"
        base_dir = env.get("HOME")

        if work_tree is None:
            clone_cmd = [*git_cmd, "clone", git_dir, url]
        else:
            clone_cmd = [*git_cmd, "clone", git_dir, url, work_tree]

        yield action(clone_cmd, env=env)

    def status(self, action: Action, argv: ArgV, env=os.environ):
        yield action(["/bin/sh", "-c", "true"], env=env)

    def forget(self, action: Action, argv: ArgV, env=os.environ):
        """Remove files from index without deleting."""
        if shutil.which("git") is None:
            raise FileNotFoundError(5, "Command not found", "git")

        raise NotImplementedError("git rm --cached <files>")

    def git(self, action: Action, argv: ArgV, env=os.environ, **options):
        """
        Run generic git commands. Unlike other functions such as 'init'
        and 'clone', this function doesn't parse options from its argv
        parameter. Therefore, options must be provided as named
        arguments.
        """
        if shutil.which("git") is None:
            raise FileNotFoundError(5, "Command not found", "git")

        name = options.get("name", "")
        configs = self.configs
        base_dir = options.get("base_dir", configs.base_dir)
        git_dir = options.get("git_dir", configs.get(name, "git_dir"))
        work_tree = options.get("work_tree", configs.get(name, "work_tree"))

        if git_dir is None:
            raise RuntimeError("git directory was not provided")

        git_cmd = list(self._generate(
            name, base_dir=base_dir, git_dir=git_dir, work_tree=work_tree
        ))
        yield action([*git_cmd, *argv])

    def _generate(self, name, **options):
        configs = self.configs

        yield "git"

        base_dir = options.get("base_dir", configs.base_dir)
        if base_dir is not None:
            yield "-C"
            yield base_dir

        git_dir = options.get("git_dir", configs.get(name, "git_dir"))
        if git_dir is not None:
            yield f"--git-dir={git_dir}"

        work_tree = options.get("work_tree", configs.get(name, "work_tree"))
        if work_tree is not None and work_tree != "":
            yield f"--work-tree={work_tree}"
