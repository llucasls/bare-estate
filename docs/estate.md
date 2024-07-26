# estate

    estate [options] <command> [<args>]

## Options:

    -v, --version
        Print the version number to standard output. If the version number
        can't be retrieved, return 1 to the shell.

    -n, --dry-run
        Print the used git commands to standard output without executing.

    -c <path>, --config=<path>
        Choose a custom path for the config file.

    -r <name>, --repo=<name>
        Choose a repository on which to apply git commands.

    -d <git-dir>, --git-dir=<git-dir>
        Choose a custom path for the git directory.

    -t <directory>, --work-tree=<directory>
        Choose a custom path as the root directory of a repository's
        work tree.

    -C <base-directory>
        Choose a base directory for git commands. If provided, git-dir and
        work-tree can be used as relative paths branching from the base
        directory.

## Environment Variables:

    GIT_DIR
        Set the location of the git directory.

    GIT_WORK_TREE
        Set the path to the root of the work tree.
