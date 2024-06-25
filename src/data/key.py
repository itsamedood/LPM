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


from cryptography.fernet import Fernet
from os import getenv
from out import LpmError
from sys import platform


class Key:
  """Representation of your encryption key."""

  HOME  = getenv("HOME") if platform == "linux" or "darwin" else f'{getenv("HOMEDRIVE")}{getenv("HOMEPATH")}'
  BASPATH = f"{HOME}/.lpm" if HOME is not None else None
  KEYPATH = f"{BASPATH}/.key" if HOME is not None else None
  as_bytes: bytes
  """ The actual key in `bytes` form. """

  def __init__(self, _bytes: bytes | None) -> None: self.as_bytes = self.write(self.gen()) if _bytes is None else _bytes

  def gen(self) -> bytes:
    """Generates key & writes it to `.key`."""

    self.as_bytes = Fernet.generate_key()
    return self.as_bytes

  def write(self, _key: bytes | None) -> bytes:
    """ Writes `_key` to `.key`. """

    if self.KEYPATH is None: raise LpmError("could not find home path", 1)
    if _key is None: _key = self.as_bytes

    with open(self.KEYPATH, "wb") as wdotkey: wdotkey.write(_key + b'\n' + b'^' * len(_key) + b" DO NOT CHANGE!!\n")
    return _key

  def get(self) -> bytes:
    """ Gets key from `.key`. """

    if self.KEYPATH is None: raise LpmError("could not find home path", 1)
    with open(self.KEYPATH, "rb") as dotkey:
      global key; key = dotkey.readlines()[0][:-1]

    return key
