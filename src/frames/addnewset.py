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


from data.data import Data
from data.dataManager import DataManager
from frames.elements.websiteurl import WebsiteURL
from paths import Paths
from tkinter import Button, Entry, Frame, Label, Tk


class AddNewSetFrame(Frame):
  def __init__(self, _parent: Frame, _controller, _paths: Paths):
    Frame.__init__(self, _parent)
    self.paths = _paths
    self.controller = _controller

    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)

    # Create elements.
    add_label = Label(self, text="Add new set", pady=10)

    parent_label = Label(self, text="Parent:")
    parent_box = Entry(self)

    email_label = Label(self, text="Email:")
    email_box = Entry(self)

    username_label = Label(self, text="Username:")
    username_box = Entry(self)

    password_label = Label(self, text="Password:")
    password_box = Entry(self)

    add_button = Button(self, text="Add", command=self.handle_input)

    # Add elements.
    add_label.grid(row=0, column=0, columnspan=2)
    parent_label.grid(row=1, column=0)
    parent_box.grid(row=1, column=1)
    email_label.grid(row=2, column=0)
    email_box.grid(row=2, column=1)
    username_label.grid(row=3, column=0)
    username_box.grid(row=3, column=1)
    password_label.grid(row=4, column=0)
    password_box.grid(row=4, column=1)
    add_button.grid(row=5, column=0)
    WebsiteURL(self).add_my_website_link(6, 38)

  def handle_input(self) -> None:
    input_name: str = ''
    inputs: list[str] = []
    err = False

    for entry in self.winfo_children():
      if isinstance(entry, Label): input_name = entry.cget("text")[:-1]
      if isinstance(entry, Entry):
        text = entry.get()
        if len(text) < 1:
          err = True
          self.controller.err("Error!", "Missing input: '%s'." %input_name, False)
        else: inputs.append(text)

    if not err:
      DataManager(None, self.paths).new(Data(inputs[0], inputs[1], inputs[2], inputs[3]))
      success_label = Label(self, fg="green", text="Success!")
      success_label.grid(row=5, column=1)

      self.clear_entries()
      self.after(2000, success_label.grid_forget)  # Remove the label after 2 seconds.

  def clear_entries(self) -> None:
    for entry in self.winfo_children():
      if isinstance(entry, Entry): entry.delete(0, "end")
