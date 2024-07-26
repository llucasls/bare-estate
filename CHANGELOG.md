## 0.6.0 - 2024-07-26

### Added

- Revamped repository management: This update replaces the previous single
bare repository approach with support for multiple non-bare repositories to
manage dotfiles.

## 0.5.0 - 2023-12-19

### Added

- Checks if the `git` executable is available in the user's PATH.

### Fixed

- Removes dependency on the `rsync` executable. Bare Estate now uses the
standard library for copying files when cloning a remote repository.

## 0.4.0 - 2023-06-25

### Added

- Add support for the XDG_DATA_HOME environment variable.

### Fixed

- Fix application when no config file is found.

## 0.3.0 - 2023-06-03

### Added

- Add base directory to config options. Now you can create repositories using
other directories as base, instead of just HOME.
- Add support for default configs. Now the program works even without a
configuration file, or with missing fields.

## 0.2.0 - 2023-04-01

### Fixed

- Changed import statements. The main script imports modules from bare_estate/
directory, instead of src/.

## 0.1.0 - 2023-02-26

### Added

- Released version 0.1. The app has functions for initializing, cloning and
managing bare repositories in general.
