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


from tkinter import Tk, Toplevel, Label, Button


class Error:
  def __init__(self, _root: Tk) -> None:
    self.root = _root

  def throw(self, _error: str) -> None:
    window = Toplevel(self.root)
    window.title("Error!")
    window.resizable(False, False)

    err_msg = Label(window, text=_error)
    err_msg.grid(padx=20, pady=20)

    close_button = Button(window, text="Close", command=window.destroy)
    close_button.grid(pady=10)

    window.geometry("+{}+{}".format(
      int(self.root.winfo_screenwidth() / 2 - window.winfo_reqwidth() / 2),
      int(self.root.winfo_screenheight() / 2 - window.winfo_reqheight() / 2)
    ))
