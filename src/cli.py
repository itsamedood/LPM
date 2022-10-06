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

from os import getenv, path
from data.dataManager import DataManager
from out import LpmError


class Cli:
    """Handles the command-line side of LPM."""

    args: list[str]
    dm = DataManager()
    help = "\n".join([
        "Usage: lpm --flag | command [args]",
        "Commands:",
        "╭─ new",
        "⏐  get",
        "⏐  list",
        "⏐  edit",
        "╰─ rm",
        "Flags:",
        "╭─ --v",
        "╰─ --h",
    ])

    def __init__(self, args: list[str]) -> None:
        self.args = args

    def process_args(self) -> None:
        command = self.args[1] if len(self.args) > 1 else None
        flag = self.args[1] if len(self.args) > 1 and (self.args[1][:2] == "--" and len(self.args[1]) > 2) else None

        if flag is not None and len(flag) > 2:
            match flag[2]:
                case "v" | "version":
                    print("v0.0.1")

                case "h" | "help":
                    print(self.help)

                case _:
                    raise LpmError(f"invalid flag: '{flag}'", 1)

        else:
            HOME = getenv("HOME")
            PATH = f"{HOME}/.lpm/lpm.bin" if HOME is not None else None

            if PATH is None:
                raise LpmError("could not find home path", 1)

            # No need to check if the path exists, because DataManager.__init__ checks.
            with open(PATH, "a") as lpmBin:
                match command:
                    case "new":
                        self.dm.new(lpmBin, self.dm.get_new_data())

                    case "get":
                        raise LpmError("not implemented yet", 0)

                    case "edit":
                        raise LpmError("not implemented yet", 0)

                    case "list":
                        raise LpmError("not implemented yet", 0)

                    case "rm":
                        raise LpmError("not implemented yet", 0)

                    case None:
                        print(self.help)

                    case cmd:
                        raise LpmError(f"invalid command: '{cmd}'", 0)
