from os import getenv, path
from out import LpmError
from sys import platform


class Paths:
    def __init__(self) -> None:
        self.HOME = getenv("HOME") if platform == "linux" or platform == "darwin" else f'{getenv("HOMEDRIVE")}{getenv("HOMEPATH")}'
        if self.HOME is None: raise LpmError("could not find home path", 1)

        self.construct_paths()

    def construct_paths(self):
        if platform == "linux" or platform == "darwin":
            self.BASPATH = f"{self.HOME}/.lpm"
            self.BINPATH = f"{self.BASPATH}/lpm.bin"  # Path to file where all data is stored.
            self.KEYPATH = f"{self.BASPATH}/.key"  # Path to where your encryption key is stored.

        else:
            self.BASPATH = f"{self.HOME}\\.lpm"
            self.BINPATH = f"{self.BASPATH}\\lpm.bin"
            self.KEYPATH = f"{self.BASPATH}\\.key"

    def paths_exist(self):
        if not path.exists(self.BASPATH): raise LpmError(f"'{self.BASPATH}' does not exist. run `lpm setup`", 0)
        if not path.exists(self.KEYPATH): raise LpmError(f"'{self.KEYPATH}' does not exist. run `lpm setup`", 0)
        if not path.exists(self.BINPATH): raise LpmError(f"'{self.BINPATH}' does not exist. run `lpm setup`", 0)
