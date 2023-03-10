#!/usr/bin/env python
import sys
import re

import toml


def bump(version: str, bumped_segment=None) -> str:
    data: object = toml.loads(version)
    version_identifier: str = data["version"]

    exp = re.compile(r"\d+(\.\d+){0,2}")
    _, release_index, *_ = exp.match(version_identifier).span()

    release = version_identifier[:release_index]
    pre_release = version_identifier[release_index:]

    size = len(release.split("."))
    major, minor, micro, *_ = map(int, [*release.split("."), 0, 0])

    if bumped_segment == "major":
        major += 1
        minor = 0
        micro = 0
        pre_release = ""
    elif bumped_segment == "minor":
        minor += 1
        micro = 0
        pre_release = ""
    elif bumped_segment == "micro" or bumped_segment == "patch":
        micro += 1
        pre_release = ""

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
    try:
        _, input_file, bumped_segment, *_ = sys.argv
    except IndexError:
        sys.exit(1)

    content = read_file(input_file)

    get_version = lambda line: line.find("version") != -1
    has_version = [entry for entry in map(get_version, content)]

    version_index = has_version.index(True)
    version = content[version_index]

    version = bump(version, bumped_segment)
    content[version_index] = version

    with open(input_file, "w") as file:
        for line in content:
            file.write(line)


if __name__ == "__main__":
    main()
