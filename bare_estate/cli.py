import sys
import getopt
import os
import subprocess as sp

from bare_estate import __version__
import bare_estate.commands as cmd
from bare_estate.config import Configs


SHORT_OPTS = "vnc:r:d:t:C:"
LONG_OPTS = [
    "version",
    "dry-run",
    "config=",
    "repo=",
    "git-dir=",
    "work-tree=",
]


def main(argv=sys.argv, /):
    opts, args = getopt.getopt(argv[1:], SHORT_OPTS, LONG_OPTS)
    status = 0

    if len(args) > 0:
        cmd_name = args[0]
    else:
        cmd_name = "estate"

    dry_run = False
    config_file = None
    options = {}
    for flag, value in opts:
        if flag in ("-v", "--version") and __version__ is None:
            return 1
        elif flag in ("-v", "--version"):
            print("bare-estate version", __version__)
            return 0
        elif flag in ("-n", "--dry-run"):
            dry_run = True
        elif flag in ("-c", "--config"):
            config_file = value
        elif flag in ("-r", "--repo"):
            options["name"] = value
        elif flag in ("-d", "--git-dir"):
            options["git_dir"] = value
        elif flag in ("-t", "--work-tree"):
            options["work_tree"] = value
        elif flag == "-C":
            options["base_dir"] = value

    config = Configs(config_file)
    command = cmd.Command(config)
    run = command.dry_run if dry_run else command.run
    config_file_exists = os.access(command.configs.filename, os.F_OK)

    def update_configs(configs: Configs):
        if config_file_exists:
            with open(configs.filename, mode="w") as file:
                configs.dump(file)
        else:
            configs.create_config_file()

    try:
        if cmd_name == "estate":
            run("status", args)
        elif cmd_name == "init" and dry_run:
            run("init", args)
            print("TOML configuration written to file:", config.filename)
            command.configs.dump(sys.stdout)
        elif cmd_name == "init":
            run("init", args)
            update_configs(command.configs)
        elif cmd_name == "clone" and dry_run:
            run("clone", args)
            print("TOML configuration written to file:", config.filename)
            command.configs.dump(sys.stdout)
        elif cmd_name == "clone":
            run("clone", args)
            update_configs(command.configs)
        else:
            run(command.git, args, **options)
    except RuntimeError as err:
        print("Error:", err, file=sys.stderr)
        status = 1

    return status
