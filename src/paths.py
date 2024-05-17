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
