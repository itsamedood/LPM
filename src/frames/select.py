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


from frames.elements.websiteurl import WebsiteURL
from paths import Paths
from tkinter import Button, Frame, Label, Tk


class SelectFrame(Frame):
  def __init__(self, _parent: Frame, _controller, _paths: Paths):
    """ `_controller` is of type `GUI`, but can't be annotated or else there will be a circular import. """

    Frame.__init__(self, _parent)
    self.paths = _paths
    self.controller = _controller

    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)

    # Create elements.
    select_label = Label(self, text="Select a procedure", pady=10)
    new_button = Button(self, text="New set", command=lambda: self.controller.show_frame("NewSetFrame"))
    get_button = Button(self, text="Get set", command=lambda: print("GET DATA"))
    edit_button = Button(self, text="Edit set", command=lambda: print("EDIT DATA"))
    list_button = Button(self, text="List sets", command=lambda: print("LIST DATA"))
    search_button = Button(self, text="Search", command=lambda: print("SEARCH FOR DATA"))
    rm_button = Button(self, text="Remove set", command=lambda: print("REMOVE DATA"))
    wipe_button = Button(self, text="Wipe sets", command=lambda: print("WIPE DATA"))
    export_button = Button(self, text="Export data", command=lambda: print("EXPORT DATA"))
    gen_button = Button(self, text="Generate Password", command=lambda: print("GENERATE PASSWORD"))
    setup_button = Button(self, text="Setup LPM", command=lambda: print("SETUP LPM"))

    # Add elements.
    select_label.grid(row=0, column=0, columnspan=2)
    new_button.grid(row=1, column=0)
    get_button.grid(row=1, column=1)
    edit_button.grid(row=2, column=0)
    list_button.grid(row=2, column=1)
    search_button.grid(row=3, column=0)
    rm_button.grid(row=3, column=1)
    wipe_button.grid(row=4, column=0)
    export_button.grid(row=4, column=1)
    gen_button.grid(row=5, column=0)
    setup_button.grid(row=5, column=1)
    WebsiteURL(self).add_my_website_link(6, 38)
