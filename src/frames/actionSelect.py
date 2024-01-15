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


from frames.baseFrame import BaseFrame
from paths import Paths
from tkinter import Frame, Label, Tk


class ActionSelectFrame(BaseFrame):
  def __init__(self, _root: Tk, _paths: Paths) -> None:
    self.root, self.paths = _root, _paths

  def build_frame(self) -> Frame:
    self.frame = Frame(self.root)

    self.root.columnconfigure(0, weight=1)
    self.root.columnconfigure(1, weight=1)

    # Create elements.
    select_label = Label(self.root, text="Select an action.", pady=10)

    # Add elements to window.
    select_label.grid(row=0, column=0, columnspan=2)

    return self.frame
