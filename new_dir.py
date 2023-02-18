import os
import tempfile
import subprocess as sp


with tempfile.TemporaryDirectory() as tmp_dir1:
    print("created directory", tmp_dir1)

    command = ["git",
               "clone",
               "https://github.com/llucasls/netbsd-home.git",
               f"{tmp_dir1}/dotfiles"]

    sp.run(command, stdout=sp.DEVNULL)

    print(os.listdir(f"{tmp_dir1}/dotfiles"))
