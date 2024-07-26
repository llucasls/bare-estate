# estate init

    estate init [options] <name> [<directory>]

This command creates a new repository using default configurations and adds
its repo's configs to the configuration file.

You can pass an optional argument with the path to a directory. If provided,
it is taken as the work tree of the new repository. By default, the work
tree is the base directory present in the configuration file.

## Options:

    -d <git-dir>, --git-dir=<git-dir>
        Choose a custom directory for the repo's metadata, taken as a
        relative path to the general git_dir from the config file. You
        can also provide an absolute path instead. It defaults to the
        name of the repo.

    -u <url>, --url=<url>
        Set the url to the remote repository. (not implemented)
