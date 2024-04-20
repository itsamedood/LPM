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


from cli import Cli
from frames.newset import NewSetFrame
from frames.select import SelectFrame
from paths import Paths
from PIL import Image, ImageTk
from tkinter import Frame, Tk, messagebox


# Thank God for StackOverflow, I could not figure out frames for the life of me lmao
class GUI(Tk):
  """ Handles the GUI side of LPM. """

  def __init__(self, *args, **kwargs):
    Tk.__init__(self, *args, **kwargs)
    self.bind("<Key>", self.on_esc)
    self.paths = Paths()

    # Initializing main window.
    self.title("LPM (ESC to return to select)")
    self.iconbitmap("assets/lpm-logo.ico")
    self.iconphoto(True, ImageTk.PhotoImage(Image.open("assets/lpm-logo.ico")))
    self.geometry("320x240")
    self.resizable(False, False)

    # Initializing container where frames will be placed.
    self.container = Frame(self)
    self.container.pack(side="top", fill="both", expand=True)
    self.container.grid_rowconfigure(0, weight=1)
    self.container.grid_columnconfigure(0, weight=1)

    self.frames: dict[str, Frame] = {}

    # Add each new frame here.
    for F in (
      SelectFrame,
      NewSetFrame,
    ):
      name = F.__name__
      frame = F(self.container, self, self.paths)
      self.frames[name] = frame

      frame.grid(row=0, column=0, sticky="nsew")

    self.show_frame("SelectFrame")  # Initial frame.

  def show_frame(self, _frame_name: str) -> None:
    try: self.frames[_frame_name].tkraise()
    except KeyError: raise Exception("%s FRAME DOESN'T EXIST." %_frame_name)

  def on_esc(self, _event):
    if _event.keysym == "Escape": self.show_frame("SelectFrame")

  def err(self, _title: str, _message: str, _close=False) -> str:
    """ Creates a small error window and displays `_message`. """

    response = messagebox.showerror(_title, _message)
    if _close: self.destroy()

    return response


if __name__ == "__main__": GUI().mainloop()
