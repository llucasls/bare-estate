# estate clone

    estate clone [options] <url> [<directory>]

It clones the repository using a url given as an argument. The name is
inferred from the url, if not provided.

If you provide the path to a directory as an extra argument, it is used
as the repository's work tree. If not, it defaults to the base directory.

## Options:

    -r <name>, --repo=<name>
        Choose a custom name for the repository.

    -d <git-dir>, --git-dir=<git-dir>
        Choose a custom directory for the repo's metadata, taken as a
        relative path to the general git_dir from the config file. You
        can also provide an absolute path instead. It defaults to the
        name of the repo.
