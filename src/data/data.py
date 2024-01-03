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

from dataclasses import dataclass
from out import Ansi


@dataclass(frozen=True, init=True)
class Data:
  """Immutable LPM data."""

  parent: str
  email: str
  username: str
  password: str

  @property
  def formatted(self) -> str: return f"{self.parent}::{self.email}::{self.username}::{self.password}"

  @property
  def as_tuple(self) -> tuple[str, str, str, str]: return (self.parent, self.email, self.username, self.password)

  def print_out(self) -> None:
    print(f"{Ansi.text.YELLOW}Parent{Ansi.special.RESET}: {Ansi.style.LIGHT}{self.parent}{Ansi.special.RESET}")
    print(f"{Ansi.text.YELLOW}Email{Ansi.special.RESET}: {Ansi.style.LIGHT}{self.email}{Ansi.special.RESET}")
    print(f"{Ansi.text.YELLOW}Username{Ansi.special.RESET}: {Ansi.style.LIGHT}{self.username}{Ansi.special.RESET}")
    print(f"{Ansi.text.YELLOW}Password{Ansi.special.RESET}: {Ansi.style.LIGHT}{self.password}{Ansi.special.RESET}")
