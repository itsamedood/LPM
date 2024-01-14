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


from paths import Paths
from tkinter import Tk, messagebox


class GUI:
  """ GUI for LPM. """

  def __init__(self) -> None:
    self.paths = Paths()
    self.current_frame = None

    # Create window.
    self.root = Tk()
    self.root.title("LPM - itsamedood")
    self.root.geometry("320x240")
    self.root.resizable(False, False)

  def err(self, _title: str, _message: str) -> str:
    """ Creates a small error window and displays `_message`. """

    response = messagebox.showerror(_title, _message)
    return response

  def run(self) -> None: self.root.mainloop()


GUI().run()
