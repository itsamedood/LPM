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


from sys import exit


class TextStyle:
    """Changes the font style. Ranges from `0` to `5`."""

    NORMAL      = "\033[0m"
    BOLD        = "\033[1m"
    LIGHT       = "\033[2m"
    ITALICIZED  = "\033[3m"
    UNDERLINED  = "\033[4m"
    BLINK       = "\033[5m"


class TextColor:
    """Changes the font color. Ranges from `30` to `37`."""

    BLACK   = "\033[0;30m"
    RED     = "\033[0;31m"
    GREEN   = "\033[0;32m"
    YELLOW  = "\033[0;33m"
    BLUE    = "\033[0;34m"
    PURPLE  = "\033[0;35m"
    CYAN    = "\033[0;36m"
    WHITE   = "\033[0;37m"


class BGColor:
    """Changes the color of the background. Ranges from `40` to `47`"""

    BLACK   = "\033[0;40m"
    RED     = "\033[0;41m"
    GREEN   = "\033[0;42m"
    YELLOW  = "\033[0;43m"
    BLUE    = "\033[0;44m"
    PURPLE  = "\033[0;45m"
    CYAN    = "\033[0;46m"
    WHITE   = "\033[0;47m"


class Special:
    """Preset color codes for quicker usage."""

    SUCCESS = "\033[1;32m"
    WARNING = "\033[1;33m"
    ERROR   = "\033[1;31m"
    RESET   = "\033[0;0;0m"


class Ansi:
    """Class for using ANSI color codes."""

    style   = TextStyle()
    text    = TextColor()
    bg      = BGColor()
    special = Special()


class LpmError(BaseException):
    """Represents an error from LPM."""

    def __init__(self, _message: str, _code: int) -> None: print(f"lpm: {Ansi.special.ERROR}error{Ansi.special.RESET}: {_message}."); return exit(_code)


def success(_message: str) -> None: return print(f"lpm: {Ansi.special.SUCCESS}success{Ansi.special.RESET}: {_message}.")
def warn(_message: str) -> None: return print(f"lpm: {Ansi.special.WARNING}warn{Ansi.special.RESET}: {_message}.")
def notify(_message: str) -> None: return print(f"lpm: {Ansi.style.LIGHT}note{Ansi.special.RESET}: {_message}.")
