import sys
from collections import defaultdict

try:
    import bare_estate.commands as cmd
except ImportError:
    import commands as cmd


commands_dict = {
    "init": cmd.init,
    "clone": cmd.clone,
    "forget": cmd.forget
}
commands_dict = defaultdict(lambda: cmd.git, commands_dict)


def main():
    status = 0

    try:
        command = cmd.cli_args[0]
        status = commands_dict[command]()

    except cmd.CommandNotFoundError as err:
        msg = "%s: %s" % (err.strerror, err.filename)
        cmd.log_err(msg)
        status = 5

    except FileNotFoundError:
        cmd.log_err("Error: the repository has not been initialized yet.")
        cmd.log_err("You can create a new repository using the command:\n")
        cmd.log_err("estate init")
        status = 2

    except cmd.NotARepositoryError as error:
        message = error.strerror
        cmd.log_err(message)
        status = 3

    except NotADirectoryError as error:
        file = error.filename
        cmd.log_err(f"Error: A file with the name {file} already exists.")
        status = 3

    except IndexError:
        cmd.log_err("Error: no command was provided to git")
        status = 4

    return status
