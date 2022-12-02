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

from os import getenv
from random import randint
from data.dataManager import DataManager
from out import LpmError, success, warn


class Cli:
    """Handles the command-line side of LPM."""

    args: list[str]
    dm: DataManager
    help = "\n".join([
        "Usage: lpm --flag | command [arg]",
        "Commands:",
        "╭─ new",
        "⏐  get <parent>",
        "⏐  edit <parent>",
        "⏐  list",
        "⏐  rm <parent>",
        "⏐  wipe",
        "⏐  export [decrypted]",
        "⏐  gen <len>",
        "╰─ setup",
        "Flags:",
        "╭─ --v",
        "╰─ --h",
    ])

    def __init__(self, _args: list[str]) -> None:
        self.args = _args
        self.dm = DataManager(_args[1] if len(_args) > 1 else None)

    def gen_password(self, _length: str | None) -> str:
        if _length is None: raise LpmError("missing argument 'length'", 1)
        length: int | None = None

        while _length.isdigit():  # All because of what I swear must be a Python3.10+ bug...
            try: length = int(_length); break
            except: continue

        if length is None: raise LpmError("password length must be an integer", 1)
        elif length >= 1000: warn("This may take longer than usual..")

        pw, chars = "", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]};:'\",<.>/?|"
        for _ in range(length): pw += chars[randint(0, len(chars)-1)]
        return pw

    def process_args(self) -> None:
        command = self.args[1] if len(self.args) > 1 else None
        flag = self.args[1] if len(self.args) > 1 and (self.args[1][:2] == "--" and len(self.args[1]) > 2) else None

        if flag is not None and len(flag) > 2:
            match flag[2]:
                case "v" | "version": print("v0.0.1")
                case "h" | "help": print(self.help)
                case _: raise LpmError(f"unknown flag: '{flag}'", 1)

        else:
            HOME = getenv("HOME")
            PATH = f"{HOME}/.lpm/lpm.bin" if HOME is not None else None
            param = self.args[2] if len(self.args) > 2 else None

            if PATH is None: raise LpmError("could not find home path", 1)

            match command:
                case "new": self.dm.new(self.dm.get_data())
                case "get": self.dm.get(param).print_out()
                case "edit": self.dm.edit(param)
                case "list": self.dm.list()
                case "rm": self.dm.rm(param)
                case "wipe": self.dm.wipe()
                case "export": self.dm.export(param)
                case "gen": success(self.gen_password(param))
                case "setup": ...

                case None: print(self.help)
                case cmd: raise LpmError(f"unknown command: '{cmd}'", 0)
