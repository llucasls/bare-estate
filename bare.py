#!/usr/bin/env python
"""
function bare --wraps='git --git-dir=/home/lucas/.dotfiles/ --work-tree=/home/lucas' --description 'manage dotfiles using a bare repository'
  git --git-dir=/home/lucas/.dotfiles/ --work-tree=/home/lucas $argv; 
end
"""
import sys
import subprocess as sp

from config import configs


cli_args = sys.argv[1:]


def git():
    proc = sp.Popen(["git", *cli_args])
    proc.communicate()
    return proc.returncode


def main():
    status = git()
    return status


if __name__ == "__main__":
    sys.exit(main())
