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


from frames.actionSelect import ActionSelectFrame
from paths import Paths
from PIL import Image, ImageTk
from tkinter import Frame, Tk, messagebox


class GUI:
  """ GUI for LPM. """

  def __init__(self) -> None:
    self.paths = Paths()
    self.current_frame: Frame | None = None

    # Create window.
    self.root = Tk()
    self.root.title("LPM - https://itsamedood.github.io")
    self.root.iconbitmap("assets/lpm-logo.ico")
    self.root.iconphoto(True, ImageTk.PhotoImage(Image.open("assets/lpm-logo.ico")))
    self.root.geometry("320x240")
    self.root.resizable(False, False)

    self.init_all_frames()
    self.show_frame(self.action_select_frame.build_frame())

  def err(self, _title: str, _message: str) -> str:
    """ Creates a small error window and displays `_message`. """

    response = messagebox.showerror(_title, _message)
    return response

  def init_all_frames(self) -> None:
    """ Initializes all frames so they can be built and displayed when needed. """

    self.action_select_frame = ActionSelectFrame(self.root, self.paths)

  def show_frame(self, _frame: Frame) -> None:
    """ Hide previous frame and tkraise `_frame` to display it. """

    if self.current_frame is not None:
      self.current_frame.grid_remove()

    _frame.grid()
    _frame.tkraise()
    self.current_frame = _frame

  def run(self) -> None: self.root.mainloop()


GUI().run()
