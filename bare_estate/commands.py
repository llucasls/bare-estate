import os
import sys
import subprocess as sp
import errno
import tempfile
import shutil

from bare_estate.config import configs


class NotARepositoryError(NotADirectoryError):
    pass


class CommandNotFoundError(FileNotFoundError):
    pass


cli_args = sys.argv[1:]
bare_cmd = ["git",
            f"--git-dir={configs['history_location']}",
            f"--work-tree={configs['base_directory']}"]


log_err = lambda message: print(message, file=sys.stderr)


def validate_file_type(file_stats):
    file_entry, file_type = file_stats
    error_message = f"{configs['history_location']} is not a bare repository"

    if file_type == "file" and not file_entry.is_file():
        raise NotARepositoryError(
            errno.ENOTDIR,
            error_message,
            configs["history_location"]
        )
    if file_type == "directory" and not file_entry.is_dir():
        raise NotARepositoryError(
            errno.ENOTDIR,
            error_message,
            configs["history_location"]
        )


def get_file_stats(bare_repo_files):
    stats_list = []
    for file in bare_repo_files:
        if file.name in ["HEAD", "config", "description"]:
            stats_list.append([file, "file"])
        elif file.name in ["branches", "hooks", "info", "objects", "refs"]:
            stats_list.append([file, "directory"])

    return stats_list


def history_dir_exists():
    bare_repo_files = []
    for file in os.scandir(configs["history_location"]):
        bare_repo_files.append(file)

    bare_repo_files.sort(key=lambda file: file.name)
    file_stats = get_file_stats(bare_repo_files)

    for file in file_stats:
        validate_file_type(file)


def init():
    if shutil.which("git") is None:
        raise CommandNotFoundError(5, "Command not found", "git")

    init_cmd = ["git", "init", "--bare", configs["history_location"]]
    config_cmd = [*bare_cmd, "config", "status.showUntrackedFiles", "no"]

    status = sp.run(init_cmd).returncode
    status += sp.run(config_cmd).returncode

    return status


def clone():
    if shutil.which("git") is None:
        raise CommandNotFoundError(5, "Command not found", "git")

    status = 1
    repository = cli_args[1]

    with tempfile.TemporaryDirectory() as tmp_dir:
        clone_cmd = ["git",
                     "clone",
                     "--quiet",
                     f"--separate-git-dir={configs['history_location']}",
                     repository,
                     f"{tmp_dir}/dotfiles"]

        config_cmd = [*bare_cmd, "config", "status.showUntrackedFiles", "no"]

        status = sp.run(clone_cmd).returncode

        shutil.copytree(f"{tmp_dir}/dotfiles", f"{configs['base_directory']}",
                        ignore=shutil.ignore_patterns(".git"),
                        dirs_exist_ok=True)

        status += sp.run(config_cmd).returncode

    return status


def forget():
    if shutil.which("git") is None:
        raise CommandNotFoundError(5, "Command not found", "git")

    history_dir_exists()
    files = sys.argv[2:]
    status = sp.run([*bare_cmd, "rm", "--cached", *files]).returncode

    return status


def git():
    if shutil.which("git") is None:
        raise CommandNotFoundError(5, "Command not found", "git")

    history_dir_exists()

    status = sp.run([*bare_cmd, *cli_args]).returncode

    return status
