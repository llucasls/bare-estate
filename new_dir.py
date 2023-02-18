import os
import tempfile
import subprocess as sp

from config import configs, HOME
from commands import bare_cmd


with tempfile.TemporaryDirectory() as tmp_dir:
    print("created directory", tmp_dir)

    clone_command = ["git",
                     "clone",
                     "--quiet",
                     f"--separate-git-dir={configs['history_location']}",
                     "https://github.com/llucasls/netbsd-home.git",
                     f"{tmp_dir}/dotfiles"]

    rsync_command = ["rsync",
                     "--recursive",
                     "--verbose",
                     "--exclude",
                     ".git",
                     f"{tmp_dir}/dotfiles/",
                     f"{HOME}/"]

    config_command = [*bare_cmd, "config", "status.showUntrackedFiles", "no"]

    sp.run(clone_command)
    sp.run(rsync_command)
    sp.run(config_command)
