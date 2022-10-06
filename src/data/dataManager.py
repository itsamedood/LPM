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

from io import TextIOWrapper
from os import getenv, path
from sys import platform
from out import Ansi, LpmError
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

    key: Key | None
    """The key used for encrypting & decrypting data."""

    def __init__(self) -> None:
        HOME = getenv("HOME") if platform == "linux" or "darwin" else f'{getenv("HOMEDRIVE")}{getenv("HOMEPATH")}'
        BINPATH = f"{HOME}/.lpm/lpm.bin" if HOME is not None else None  # Path to file where all data is stored.
        KEYPATH = f"{HOME}/.lpm/.key" if HOME is not None else None  # Path to where your encryption key is stored.

        # Probably won't ever happen.
        if KEYPATH is None or BINPATH is None:
            raise LpmError("could not find home path", 1)

        # Verifying `.key` exists, and that it contains a string.
        if path.exists(KEYPATH):
            with open(KEYPATH, "rb") as rdotkey:  # For reading.
                lines = rdotkey.readlines()

                if len(lines) < 1:
                    with open(KEYPATH, "wb") as wdotkey:  # For writing.
                        key = Key(None).gen()
                        carets = ""
                        for _ in key: carets += "^"

                        wdotkey.write(key + bytes(carets[:-1], encoding="ascii") + b" DO NOT CHANGE!!\n")
                    lines = rdotkey.readlines()  # Re-read lines.

                self.key = Key(lines[0][:-1])  # To get avoid encoding `\n`.
        else:
            # Code to create `.key`.
            raise LpmError(f"'{KEYPATH}' was not found, so it was created. restart the program.", 1)

        # Verifying `lpm.bin` exists and has not been tampered with.
        if path.exists(BINPATH):
            # Get current hash (if it exists).
            # Hash data - the current hash.
            # Compare digests.
            pass


    def get_new_data(self) -> Data:
        """Gets data from the user to store."""

        try:
            parent = input(f"{Ansi.text.GREEN}App or site this data is for{Ansi.special.RESET}: ")
            email = input(f"{Ansi.text.GREEN}Email{Ansi.special.RESET}: ")
            username = input(f"{Ansi.text.GREEN}Username{Ansi.special.RESET}: ")
            password = getpass(f"{Ansi.text.GREEN}Password (hidden){Ansi.special.RESET}: ")

            return Data(parent, email, username, password)
        except (EOFError, KeyboardInterrupt):
            print("")
            raise LpmError("cancelled", 1)

        except GetPassWarning:
            raise LpmError("failed to disable echo", 1)

    def hash(self, input: bytearray) -> int:
        """Implementation of the CRC-32 hashing algorithm."""

        num = 0xFFFFFFFF

        for i in range(len(input)):
            temp = (num ^ input[i]) & 0xFF

            for _ in range(0, 8):
                temp = (temp >> 1) ^ (-(temp & 1) & 0xEDB88320)
            num = (num >> 8) ^ temp

        return num ^ 0xFFFFFFFF

    def new(self, lpmData: TextIOWrapper, data: Data) -> None:
        """Creates a new set of data, encrypts it, and stores it."""

        parent, email, username, password = data.as_tuple
        fdata = data.formatted

        print(data.as_tuple, "\nnow to save all of this...")
