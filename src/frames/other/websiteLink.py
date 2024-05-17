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


from tkinter import Tk, Label
from webbrowser import open_new_tab


class WebsiteLink:
  def __init__(self, _root: Tk) -> None:
    self.root = _root

  def add_my_website_link(self, _row: int, _pady: int) -> None:
    link_label = Label(self.root, text="itsamedood.github.io", fg="blue", cursor="hand2")
    link_label.grid(row=_row, column=0, columnspan=2, pady=_pady, sticky="se")
    link_label.bind("<Button-1>", self._open_link)

  def _open_link(self, _event): open_new_tab("https://itsamedood.github.io")
