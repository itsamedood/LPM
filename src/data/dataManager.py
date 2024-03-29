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

from os import mkdir, path
from paths import Paths
from sys import exit
from out import Ansi, LpmError, notify, success
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
  fernet: Fernet
  param: str | None

  def __init__(self, _param: str | None, _paths: Paths) -> None:
    self.param, self.paths = _param, _paths

    if _param is not None and _param == "setup": self.setup()
    else:
      _paths.paths_exist()  # Check if paths exist.

      # Getting the key.
      with open(self.paths.KEYPATH, "rb") as rdotkey:
        lines = rdotkey.readlines()
        if len(lines) < 1: Key(None)

        self.key = Key(lines[0][:-1])  # To get avoid encoding `\n`.
      self.fernet = Fernet(self.key.as_bytes)

  def get_data(self) -> Data:
    """Gets data from the user to store."""

    try:
      parent = input(f"{Ansi.text.GREEN}App or site this data is for{Ansi.special.RESET}: ")
      email = input(f"{Ansi.text.GREEN}Email{Ansi.special.RESET}: ")
      username = input(f"{Ansi.text.GREEN}Username{Ansi.special.RESET}: ")
      password = input(f"{Ansi.text.GREEN}Password{Ansi.special.RESET}: ")

      return Data(parent, email, username, password)

    except (EOFError, KeyboardInterrupt): print(""); raise LpmError("cancelled", 1)

  def encrypt(self, _data: bytes) -> bytes: return self.fernet.encrypt(_data)
  def decrypt(self, _data: bytes) -> bytes: return self.fernet.decrypt(_data)

  def new(self, data: Data) -> None:
    """Encrypts the data & stores it."""

    if self.exists(data.parent): raise LpmError("'%s' already exists" %data.parent, 1)

    with open(self.paths.BINPATH, "ab") as lpmBin: lpmBin.write(self.encrypt(bytes(f"{data.formatted}", encoding="ascii")) + b"\n")
    return success(f"'{data.as_tuple[0]}' was saved")

  def get(self, _parent: str | None) -> Data:
    if _parent is None: raise LpmError("missing argument 'parent'", 1)

    with open(self.paths.BINPATH, "rb") as lpmBin:
      lines = [self.decrypt(eline) for eline in lpmBin.readlines()]

      for line in lines:
        line_split = str(line)[2:-1].split("::")
        if line_split[0] == _parent: return Data(line_split[0], line_split[1], line_split[2], line_split[3])

      raise LpmError(f"'{_parent}' does not exist", 1)

  def exists(self, _parent: str | None) -> bool:
    if _parent is None: return False

    with open(self.paths.BINPATH, "rb") as lpmBin:
      lines = [self.decrypt(eline) for eline in lpmBin.readlines()]

      for line in lines:
        line_split = str(line)[2:-1].split("::")
        if line_split[0] == _parent: return True

      return False

  def edit(self, _parent: str | None) -> None:
    if _parent is None: raise LpmError("missing argument 'parent'", 1)

    self.get(_parent)  # Verifies this data exists.
    data = self.get_data()

    with open(self.paths.BINPATH, "rb") as rlpmBin:
      _lines = [self.decrypt(l) for l in rlpmBin.readlines()]
      lines: list[bytes] = []

      for line in _lines:
        if str(line)[2:-1].split("::")[0] != _parent: lines.append(self.encrypt(line))
        else: lines.append(self.encrypt(bytes(data.formatted, encoding="ascii")))

      with open(self.paths.BINPATH, "wb") as wlpmBin: [wlpmBin.write(line + b"\n") for line in lines]

    return success(f"edited '{_parent}'" if _parent == data.parent else f"edited '{_parent}' (now '{data.parent}')")

  def list(self, _display: bool = True) -> list[str]:
    with open(self.paths.BINPATH, "rb") as lpmBin:
      parents = [str(self.decrypt(l).split(b"::")[0])[2:-1] for l in lpmBin.readlines()]

      if len(parents) > 0:
        if _display:
          print("%i found:" %len(parents))
          [print(f"{Ansi.style.LIGHT}•{Ansi.special.RESET} {p}") for p in parents]

        return parents

      raise LpmError("no data found", 1)

  def search(self, _query: str | None) -> ...:
    if _query is None: raise LpmError("missing argument 'query'", 1)
    results = [p for p in self.list(False) if _query.lower() in p.lower()]

    if len(results) < 1: raise LpmError("no results found", 1)
    print("%i results found:" %len(results))
    [print(f"{Ansi.style.LIGHT}•{Ansi.special.RESET} {r}") for r in results]

  def rm(self, _parent: str | None) -> None:
    if _parent is None: raise LpmError("missing argument 'parent'", 1)

    self.get(_parent)  # Verifies this data exists.

    with open(self.paths.BINPATH, "rb") as rlpmBin:
      lines = [self.decrypt(eline) for eline in rlpmBin.readlines()]
      filtered_lines: list[bytes] = []

      for line in lines:
        if str(line)[2:-1].split("::")[0] != _parent: filtered_lines.append(self.encrypt(line))

      with open(self.paths.BINPATH, "wb") as wlpmBin: [wlpmBin.write(fline + b"\n") for fline in filtered_lines]

    return success(f"'{_parent}' was removed")

  def wipe(self) -> None:
    # if self.BINPATH is None or self.KEYPATH is None: raise LpmError("could not find home path", 1)

    with open(self.paths.BINPATH, "rb") as lpmBin:
      if len(lpmBin.readlines()) > 0:
        with open(self.paths.KEYPATH, "wb") as wdotkey: wdotkey.write(b"")
        with open(self.paths.BINPATH, "wb") as wlpmBin: wlpmBin.write(b""); return success("wiped all data and key")
      else: raise LpmError("no data found", 1)

  def export(self, _decrypted: str | None) -> None:  # Will get around to using `_decrypted` eventually.
    # if self.BINPATH is None: raise LpmError("could not find home path", 1)
    if not _decrypted == "dc": _decrypted = None  # `lpm export dc` exports all data, decrypted.

    PATH = f"{self.paths.HOME}/Desktop/export.txt"
    if path.exists(PATH): raise LpmError("data already exported", 1)

    with open(self.paths.BINPATH, "rb") as lpmBin:
      with open(PATH, "wb") as txt:
        if _decrypted is not None: txt.write(b'\n'.join([self.decrypt(l) for l in lpmBin.readlines()]))
        else: txt.write(lpmBin.read())

    return success(f"exported all data to '{PATH}'")

  def setup(self) -> None:
    if not path.exists(self.paths.BASPATH): mkdir(self.paths.BASPATH); notify(f"'{self.paths.BASPATH}' created")
    else: notify(f"'{self.paths.BASPATH}' exists")

    if not path.exists(self.paths.KEYPATH):
      self._touch(self.paths.KEYPATH); notify(f"'{self.paths.KEYPATH}' created"); Key(None)
    else: notify(f"'{self.paths.KEYPATH}' exists")

    if not path.exists(self.paths.BINPATH):
      self._touch(self.paths.BINPATH); notify(f"'{self.paths.BINPATH}' created")
    else: notify(f"'{self.paths.BINPATH}' exists")

    success("lpm is now ready"); exit(0)

  def _touch(self, _file: str) -> None:
    with open(_file, 'w') as file: ...
    file.close()
