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


from frames.addNewSet import AddNewSetFrame
from frames.baseFrame import BaseFrame
from frames.other.websiteLink import WebsiteLink
from paths import Paths
from tkinter import Tk, Frame, Label, Button


class SelectFrame(BaseFrame):
  _frames: dict[int, Frame] = {}

  def __init__(self, _root: Tk, _paths: Paths) -> None:
    self.root, self.paths = _root, _paths


  def build_frame(self) -> Frame:
    self.frame = Frame(self.root)

    self.root.columnconfigure(0, weight=1)
    self.root.columnconfigure(1, weight=1)

    # Create elements.
    select_label = Label(self.root, text="Select a procedure", pady=10)
    add_new_set_button = Button(self.root, text="Add new set", command=self.switch_ans_frame)

    # Add elements.
    select_label.grid(row=0, column=0, columnspan=2)
    add_new_set_button.grid(row=1, column=0,)
    WebsiteLink(self.root).add_my_website_link(2, 71)

    return self.frame

  def switch_ans_frame(self) -> None:
    self._switch_frame(AddNewSetFrame(self.root, self.paths))


  def _switch_frame(self, _frame: BaseFrame) -> None:
    self.frame.grid_remove()  # Remove this frames' widgets.

    _frame.grid()
    _frame.tkraise()
