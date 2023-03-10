#!/usr/bin/env python
import sys
import re
import argparse

import toml


class Release(argparse.Namespace):
    def __init__(self, args):
        self.file = args.file
        self.release = args.release
        self.pre_release = args.alpha or args.beta or args.rc


def bump_pre(pre_release, release, option):
    should_error = (
        release is None and option == "alpha" and pre_release[0] == "b" or
        release is None and option == "alpha" and pre_release[0] == "c" or
        release is None and option == "alpha" and pre_release[:2] == "rc" or
        release is None and option == "beta" and pre_release[0] == "c" or
        release is None and option == "beta" and pre_release[:2] == "rc")

    if should_error:
        print(f"Error: cannot bump to {option} pre-release", file=sys.stderr)
        sys.exit(1)

    exp = re.compile(r"\D+")
    _, pre_release_index, *_ = exp.match(pre_release).span()

    pre_letter = pre_release[:pre_release_index]
    pre_number = pre_release[pre_release_index:]
    pre_number = 0 if pre_number == "" else int(pre_number)

    should_bump_number = (
        release is None and option == "alpha" and pre_letter == "a" or
        release is None and option == "beta" and pre_letter == "b" or
        release is None and option == "rc" and pre_letter in ["c", "rc"])

    if should_bump_number:
        pre_number += 1
    else:
        pre_number = ""
        pre_letter = {"alpha": "a", "beta": "b", "rc": "rc"}[option]

    return f"{pre_letter}{pre_number}"


def bump(version: str, bumped_release=None, bumped_pre_release=None) -> str:
    data: object = toml.loads(version)
    version_identifier: str = data["version"]

    exp = re.compile(r"\d+(\.\d+){0,2}")
    _, release_index, *_ = exp.match(version_identifier).span()

    release = version_identifier[:release_index]
    pre_release = version_identifier[release_index:]

    size = len(release.split("."))
    major, minor, micro, *_ = map(int, [*release.split("."), 0, 0])

    if bumped_release == "major":
        major += 1
        minor = 0
        micro = 0
    elif bumped_release == "minor":
        minor += 1
        micro = 0
    elif bumped_release in ["micro", "patch"]:
        micro += 1

    if bumped_pre_release in ["alpha", "beta", "rc"]:
        pre_release = bump_pre(pre_release, bumped_release, bumped_pre_release)

    major, minor, micro = map(str, [major, minor, micro])
    release_list = [major, minor, micro]
    if micro != "0":
        size = max(3, size)
    elif minor != "0" and micro == "0":
        size = max(2, size)

    release = ".".join(release_list[:size])
    data["version"] = "".join([release, pre_release])

    return toml.dumps(data)


def read_file(input_file):
    content = []

    with open(input_file, "r") as file:
        for line in file.readlines():
            content.append(line)

    return content


def main():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument("file")
    parser.add_argument("release", nargs="?")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--alpha", action="store_const", const="alpha")
    group.add_argument("-b", "--beta", action="store_const", const="beta")
    group.add_argument("-c", "--rc", action="store_const", const="rc")

    args = Release(parser.parse_args())

    input_file = args.file
    release = args.release
    pre_release = args.pre_release

    content = read_file(input_file)

    get_version = lambda line: line.strip().find("version") == 0
    has_version = list(map(get_version, content))

    version_index = has_version.index(True)
    version = content[version_index]

    version = bump(version, release, pre_release)
    content[version_index] = version

    with open(input_file, "w") as file:
        for line in content:
            file.write(line)


if __name__ == "__main__":
    main()
