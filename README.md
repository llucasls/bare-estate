# Bare Estate

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

## Install

To install this package from the PyPI, you can use the command:

```sh
pip install bare-estate
```

The current version has no Python dependencies, other than the base install.
However, it requires `git` and `rsync` installed locally in order to work.

## Credits

- Greg Owen, for the [blog post](https://stegosaurusdormant.com/bare-git-repo/)
that inspired this project
- StreakyCobra and the other users from
[Hacker News](https://news.ycombinator.com/item?id=11070797)
