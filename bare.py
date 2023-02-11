#!/usr/bin/env python
"""
function bare --wraps='git --git-dir=/home/lucas/.dotfiles/ --work-tree=/home/lucas' --description 'manage dotfiles using a bare repository'
  git --git-dir=/home/lucas/.dotfiles/ --work-tree=/home/lucas $argv; 
end
"""
import sys
import subprocess as sp


cli_args = sys.argv[1:]


def git():
    print(["git", *cli_args])


if __name__ == "__main__":
    git()
