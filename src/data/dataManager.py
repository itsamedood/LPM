# Copyright (C) 2022 David Spencer
#
# This file is part of LPM.
#
# LPM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LPM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LPM.  If not, see <http://www.gnu.org/licenses/>.

from os import getenv, system, mkdir, path
from sys import platform
from out import Ansi, LpmError, notify, success
from getpass import GetPassWarning, getpass
from cryptography.fernet import Fernet
from data.key import Key
from data.data import Data


class DataManager:
    """
    Responsible for managing LPM data.

    The hash is always the first thing stored in `lpm.bin`. When hashing, the previous or current hash is ignored.
    This is used to verify data integrity.
    """

    key: Key
    """The key used for encrypting & decrypting data."""

    fernet: Fernet

    HOME    = getenv("HOME") if platform == "linux" or "darwin" else f'{getenv("HOMEDRIVE")}{getenv("HOMEPATH")}'
    BASPATH = f"{HOME}/.lpm" if HOME is not None else None
    BINPATH = f"{BASPATH}/lpm.bin" if HOME is not None else None  # Path to file where all data is stored.
    KEYPATH = f"{BASPATH}/.key" if HOME is not None else None  # Path to where your encryption key is stored.

    def __init__(self) -> None:
        # Probably won't ever happen.
        if self.BASPATH is None: raise LpmError("could not find home path", 1)
        if not path.exists(self.BASPATH): mkdir(self.BASPATH)

        # Verifying `.key` exists, and that it contains a string.
        if not path.exists(self.KEYPATH): system(f"echo > {self.KEYPATH}"); notify(f"'{self.KEYPATH}' created")

        with open(self.KEYPATH, "rb") as rdotkey:  # For reading.
            lines = rdotkey.readlines()

            if len(lines) < 1:
                with open(self.KEYPATH, "wb") as wdotkey:  # For writing.
                    key = Key(None).gen()
                    carets = ""
                    for _ in key: carets += "^"

                    wdotkey.write(key + bytes(carets[:-1], encoding="ascii") + b" DO NOT CHANGE!!\n")
                lines = rdotkey.readlines()  # Re-read lines.

            self.key = Key(lines[0][:-1])  # To get avoid encoding `\n`.

        # Verifying `lpm.bin` exists and has not been tampered with.
        if path.exists(self.BINPATH): pass
            # Get current hash (if it exists).
            # Hash data - the current hash.
            # Compare digests.

        else: system(f"echo > {self.BINPATH}"); notify(f"'{self.BINPATH}' created")

        self.fernet = Fernet(self.key.as_bytes, None)

    def get_new_data(self) -> Data:
        """Gets data from the user to store."""

        try:
            parent = input(f"{Ansi.text.GREEN}App or site this data is for{Ansi.special.RESET}: ")
            email = input(f"{Ansi.text.GREEN}Email{Ansi.special.RESET}: ")
            username = input(f"{Ansi.text.GREEN}Username{Ansi.special.RESET}: ")
            password = getpass(f"{Ansi.text.GREEN}Password (hidden){Ansi.special.RESET}: ")

            return Data(parent, email, username, password)

        except (EOFError, KeyboardInterrupt): print(""); raise LpmError("cancelled", 1)
        except GetPassWarning: raise LpmError("failed to disable echo", 1)

    def hash(self, input: bytearray) -> int:
        """Implementation of the CRC-32 hashing algorithm."""

        num = 0xFFFFFFFF

        for i in range(len(input)):
            temp = (num ^ input[i]) & 0xFF

            for _ in range(0, 8): temp = (temp >> 1) ^ (-(temp & 1) & 0xEDB88320)
            num = (num >> 8) ^ temp

        return num ^ 0xFFFFFFFF

    def encrypt(self, data: bytes) -> bytes: return self.fernet.encrypt(data)
    def decrypt(self, data: bytes) -> bytes: return self.fernet.decrypt(data)

    def new(self, data: Data) -> None:
        """Encrypts the data & stores it."""

        if self.BINPATH is None: raise LpmError("could not find home path", 1)

        with open(self.BINPATH, "ab") as lpmBin: lpmBin.write(self.encrypt(bytes(f"{data.formatted}\n", encoding="ascii")))
        success(f"'{data.as_tuple[0]}' was saved")

    def get(self, _parent: str | None) -> None:
        if self.BINPATH is None: raise LpmError("could not find home path", 1)
        if _parent is None: raise LpmError("missing argument 'parent'", 1)

        with open(self.BINPATH, "rb") as lpmBin:
            lines = [self.decrypt(eline) for eline in lpmBin.readlines()]

            for line in lines:
                line_split = str(line)[2:-3].split("::")
                if line_split[0] == _parent: return Data(line_split[0], line_split[1], line_split[2], line_split[3]).print_out()

            raise LpmError(f"'{_parent}' does not exist", 1)

    def edit(self, _parent: str | None) -> None: ...

    def list(self) -> None:
        if self.BINPATH is None: raise LpmError("could not find home path", 1)

        with open(self.BINPATH, "rb") as lpmBin:
            parents = [str(self.decrypt(l).split(b"::")[0])[2:-1] for l in lpmBin.readlines()]
            if len(parents) > 0: [print(f"{Ansi.style.LIGHT}•{Ansi.special.RESET} {p}") for p in parents]
            else: raise LpmError("no data found", 1)

    def rm(self, _parent: str | None) -> None: ...
    def wipe(self) -> None: ...
    def export(self, _decrypted: bool | None) -> None: ...
