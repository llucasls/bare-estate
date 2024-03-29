# Bare Estate

## Table of Contents

- [About](#about)
- [Configuration](#configuration)
- [Usage](#usage)
- [Install](#install)
- [Credits](#credits)

## About

Have you ever needed to install a brand new Linux distro or BSD system? Any
experient user has done this at least a couple times, and certainly has a
dotfiles repository somewhere. But how would you transfer your dotfiles? Maybe
with symbolic links, copying files from a cloned repository, flash drive or
perhaps a combination of those.

With Bare Estate you don't need a convoluted strategy for managing your
dotfiles. You can create a bare repository that will store your repository's
data. Manage your dotfiles as if they were on a regular repo. Even files from
your home directory, without actually turning your home into a git repository
itself.

And the best part is the application handles the abstraction for you,
so you can use it in the same you use git!

## Configuration

The configuration is made by using a json file. The path of the file is
`${XDG_CONFIG_HOME}/bare_estate.json`. If you didn't set the value of the
`XDG_CONFIG_HOME` environment variable, then it defaults to
`${HOME}/.config/bare_estate.json`.

### Config Options:

- history_location: it says where your bare repository directory will be
located. Environment variables don't expand. So you will have to write the
complete path of the file.
- base_directory: the directory from where you will manage all your dotfiles.
You can either put them directly in the base directory, or in subdirectories
within it.

### Examples:

bare_estate.json:
```json
{
    "history_location": "/home/lucas/.local/share/bare_estate",
    "base_directory": "/home/lucas"
}
```

## Usage

The package introduces an executable script called `estate` as the main
entrypoint for the application. It is used just like you would use git.

### Examples:

- Initialize a new repo:
```sh
estate init
```

- Clone an existing repository:
```sh
estate clone <dotfiles-repo-url>
```
**Warning**: cloning a repository will overwrite your local files if the remote
repository has files with the same name.

- Add files to the staging area:
```sh
estate add file1 file2 file3
```

- Check your repository's status:
```sh
estate status
```

- Commit your changes:
```sh
estate commit
```

- Push your changes to the remote repo:
```sh
estate push
```

## Install

To install this package from the PyPI, you can use the command:

```sh
pip install -U bare-estate
```

The current version has no Python dependencies, other than the base install.
However, it requires `git` and `rsync` installed locally in order to work.

## Credits

- Greg Owen, for the [blog post](https://stegosaurusdormant.com/bare-git-repo/)
that inspired this project
- StreakyCobra and the other users from
[Hacker News](https://news.ycombinator.com/item?id=11070797)
