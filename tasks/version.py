import re
from collections import namedtuple


class Version:
    def __init__(self, version: str):
        exp = re.compile(r"\d+(\.\d+){0,2}")
        index = exp.match(version).end()

        release = version[:index]
        pre_release = version[index:]

        self._release_size = 3
        major, minor, micro, *_ = *release.split("."), None, None

        if micro is None:
            micro = "0"
            self._release_size -= 1

        if minor is None:
            minor = "0"
            self._release_size -= 1

        exp = re.compile(r"\D+")
        index = exp.match(pre_release).end()

        pre_letter = pre_release[:index]
        pre_number = pre_release[index:]

        self.major = int(major)
        self.minor = int(minor)
        self.micro = int(micro)
        self.pre_letter = pre_letter
        self.pre_number = int(pre_number) if pre_number != "" else 0

    def bump_major(self):
        self.major += 1
        self.minor = 0
        self.micro = 0

    def bump_minor(self):
        self._release_size = max(self._release_size, 2)
        self.minor += 1
        self.micro = 0

    def bump_micro(self):
        self._release_size = max(self._release_size, 3)
        self.micro += 1

    @property
    def tuple(self):
        "return version in tuple format"
        return (self.major,
                self.minor,
                self.micro,
                self.pre_letter,
                self.pre_number)

    @property
    def string(self):
        "return version in string format"
        release_list = []
        release_list.append(str(self.major))
        if self.minor != 0 or self._release_size >= 2:
            release_list.append(str(self.minor))
        if self.micro != 0 or self._release_size == 3:
            release_list.append(str(self.micro))
        pre_letter = self.pre_letter
        pre_number = str(self.pre_number) if self.pre_number != 0 else ""
        release = ".".join(release_list)
        pre_release = f"{pre_letter}{pre_number}"
        return f"{release}{pre_release}"
