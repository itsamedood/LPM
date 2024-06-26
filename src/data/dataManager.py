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


from typing import Any
from data.data import Data
from data.key import Key
from cryptography.fernet import Fernet
from os import mkdir, path
from out import Ansi, LpmError, notify, success
from paths import Paths
from sys import exit


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
      try:
        with open(self.paths.KEYPATH, "rb") as rdotkey:
          lines = rdotkey.readlines()
          if len(lines) < 1: Key(None)

          self.key = Key(lines[0][:-1])  # To get avoid encoding `\n`.
        self.fernet = Fernet(self.key.as_bytes)
      except IndexError: raise LpmError("no key found. one has been generated", 1)

  def get_key(self) -> Key:
    with open(self.paths.KEYPATH, "rb") as rdotkey:
      lines = rdotkey.readlines()
      return Key(lines[0][:-1])

  def update_key(self) -> None:
    self.key = self.get_key()
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

  def  new(self, data: Data) -> None:
    """Encrypts the data & stores it."""

    if self.exists(data.parent): raise LpmError("'%s' already exists" %data.parent, 1)

    with open(self.paths.BINPATH, "ab") as lpmBin: lpmBin.write(self.encrypt(bytes(f"{data.formatted}", encoding="ascii")) + b"\n")
    return success(f"'{data.as_tuple[0]}' was saved")

  def get(self, _parent: str | None) -> Data:
    """ Gets a data set from `_parent`. """

    if _parent is None: raise LpmError("missing argument 'parent'", 1)

    with open(self.paths.BINPATH, "rb") as lpmBin:
      lines = [self.decrypt(eline) for eline in lpmBin.readlines()]

      for line in lines:
        line_split = str(line)[2:-1].split("::")
        if line_split[0] == _parent: return Data(line_split[0], line_split[1], line_split[2], line_split[3])

      raise LpmError(f"'{_parent}' does not exist", 1)

  def exists(self, _parent: str | None) -> bool:
    """ Checks to see if data set with `_parent` exists. """
    if _parent is None: return False

    with open(self.paths.BINPATH, "rb") as lpmBin:
      lines = [self.decrypt(eline) for eline in lpmBin.readlines()]

      for line in lines:
        line_split = str(line)[2:-1].split("::")
        if line_split[0] == _parent: return True

      return False

  def edit(self, _parent: str | None) -> None:
    """ Edit an existing data set. """

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

  # Changed as to not conflict with built-in type `list`.
  def list_sets(self, _display: bool = True) -> list[str]:
    """ Lists all data sets by parent (name). """

    with open(self.paths.BINPATH, "rb") as lpmBin:
      parents = [str(self.decrypt(l).split(b"::")[0])[2:-1] for l in lpmBin.readlines()]

      if len(parents) > 0:
        if _display:
          print("%i found:" %len(parents))
          [print(f"{Ansi.style.LIGHT}•{Ansi.special.RESET} {p}") for p in parents]

        return parents

      raise LpmError("no data found", 1)

  def search(self, _query: str | None) -> None:
    """ Searches for a data set via name. """

    if _query is None: raise LpmError("missing argument 'query'", 1)
    results = [p for p in self.list_sets(False) if _query.lower() in p.lower()]

    if len(results) < 1: raise LpmError("no results found", 1)

    print("%i results found:" %len(results))
    [print(f"{Ansi.style.LIGHT}•{Ansi.special.RESET} {r}") for r in results]

  def rm(self, _parent: str | None) -> None:
    """ Removes a data set from `lpm.bin`. """

    if _parent is None: raise LpmError("missing argument 'parent'", 1)

    self.get(_parent)  # Verifies this data exists.

    with open(self.paths.BINPATH, "rb") as rlpmBin:
      lines = [self.decrypt(eline) for eline in rlpmBin.readlines()]
      filtered_lines: list[bytes] = []

      for line in lines:
        if str(line)[2:-1].split("::")[0] != _parent: filtered_lines.append(self.encrypt(line))

      with open(self.paths.BINPATH, "wb") as wlpmBin: [wlpmBin.write(fline + b"\n") for fline in filtered_lines]

    return success(f"'{_parent}' was removed")

  def wipe(self, _print = True, _key = True, _data = True) -> None:
    """ Deletes the key (`.key`) and all saved data in `lpm.bin`. """

    with open(self.paths.BINPATH, "rb") as lpmBin:
      if len(lpmBin.readlines()) > 0:
        if _key:
          with open(self.paths.KEYPATH, "wb") as wdotkey: wdotkey.write(b'')
        if _data:
          with open(self.paths.BINPATH, "wb") as wlpmBin: wlpmBin.write(b'')

        return success("wiped all data and key")

      else: raise LpmError("no data found", 1)

  def import_data(self, _exportdottxt: str | None) -> None:
    if _exportdottxt is None: raise LpmError("cannot find %s." %_exportdottxt, 1)

    if path.exists(_exportdottxt):
      with open(_exportdottxt, 'rb') as rexportdottxt:
        global key
        global data
        global dcd
        lines = rexportdottxt.readlines()

        key = lines[0][:-1]
        dcd = bool(lines[1])  # (decrypted)
        data = [l[:-1] for l in lines[2:] if len(l) > 0]

        # print(key, dcd, data, sep='\n')

        if not dcd:
          with open(self.paths.KEYPATH, "wb"): Key(key).write(None)
          with open(self.paths.BINPATH, "wb") as wlpmbin: wlpmbin.write(b'\n'.join(data))

        else:
          with open(self.paths.KEYPATH, "wb"): Key(key).write(None)
          with open(self.paths.BINPATH, "wb") as wlpmbin:
            wlpmbin.write(b'\n'.join([self.encrypt(l) for l in data]))

    return success("successfully imported data")

  def export(self, _decrypted: str | None, _write=True) -> tuple[bytes, bytes] | tuple[None, None]:
    """
    Exports key and all saved data either:

    - Encrypted.
    - Decrypted (`lpm export dc`).
    """

    if not _decrypted == "dc": _decrypted = None  # `lpm export dc` exports all data, decrypted.

    PATH = f"{self.paths.HOME}/Desktop/export.txt"
    if _write and path.exists(PATH): raise LpmError("data already exported", 1)

    with open(self.paths.BINPATH, "rb") as lpmBin:
      if _write:
        with open(PATH, "wb") as txt:
          if _decrypted is not None: txt.write(self.key.get() + b"\n" + b"True" + b"\n\n" + b'\n'.join([self.decrypt(l) for l in lpmBin.readlines()]))
          else: txt.write(self.key.get() + b"\n" + b"False" + b"\n\n" + lpmBin.read())

        success(f"exported all data to '{PATH}'")
        return (None, None)

      else: return (self.key.get(), b'\n'.join([self.decrypt(l) for l in lpmBin.readlines()]))

  def resecure(self):
    """
    Reencrypts everything with a brand new key.

    It is recommended to backup both the old key and old encrypted data before doing this.
    """

    oldkey, databytestr = self.export('dc', False)
    if oldkey is None or databytestr is None: raise LpmError("key or data gotten for resecure is None", 1)

    self.wipe(False)  # Delete key and all saved data.
    Key(None)  # Generate new key.
    self.update_key()

    # Reecrypt data and write it to .lpm 1 at a time after clearing .lpm.
    datasets = databytestr.split(b'\n')

    for dataset in datasets:
      datastr = str(dataset)[2:-1].split("::")

      data = Data(datastr[0], datastr[1], datastr[2], datastr[3])
      self.new(data)


  def setup(self) -> None:
    """ Sets up LPM. """

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
