import sys
import subprocess as sp

from config import configs, HOME


cli_args = sys.argv[1:]
bare_cmd = ["git",
            f"--git-dir={configs['history_location']}",
            f"--work-tree={HOME}"]


def init():
    init_cmd = ["git", "init", "--bare", configs["history_location"]]
    config_cmd = [*bare_cmd, "config", "status.showUntrackedFiles", "no"]

    status = sp.run(init_cmd).returncode
    status += sp.run(config_cmd).returncode

    return status


def git():
    status = sp.run([*bare_cmd, *cli_args]).returncode

    return status
