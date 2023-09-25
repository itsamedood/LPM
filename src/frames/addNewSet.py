from data.data import Data
from data.dataManager import DataManager
from frames.baseFrame import BaseFrame
from frames.other.error import Error
from frames.other.websiteLink import WebsiteLink
from paths import Paths
from tkinter import Tk, Frame, Label, Entry, Button


class AddNewSetFrame(BaseFrame):
    def __init__(self, _root: Tk, _paths: Paths) -> None:
        self.root, self.paths = _root, _paths

    def build_frame(self) -> Frame:
        frame = Frame(self.root)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        # Create elements.
        add_label = Label(self.root, text="Add new set", pady=10)

        parent_label = Label(self.root, text="Parent:")
        parent_box = Entry(self.root)

        email_label = Label(self.root, text="Email:")
        email_box = Entry(self.root)

        username_label = Label(self.root, text="Username:")
        username_box = Entry(self.root)

        password_label = Label(self.root, text="Password:")
        password_box = Entry(self.root)

        add_button = Button(self.root, text="Add", command=self.handle_input)

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
        WebsiteLink(self.root).add_my_website_link(6, 71)

        return frame

    def handle_input(self) -> None:
        input_name: str = ''
        inputs: list[str] = []
        err = False

        for entry in self.root.winfo_children():
            if isinstance(entry, Label): input_name = entry.cget("text")[:-1]
            if isinstance(entry, Entry):
                text = entry.get()
                if len(text) < 1:
                    err = True
                    Error(self.root).throw("Missing input: '%s'." %input_name)
                else: inputs.append(text)

        if not err:
            DataManager(None, self.paths).new(Data(inputs[0], inputs[1], inputs[2], inputs[3]))
            success_label = Label(self.root, fg="green", text="Success!")
            success_label.grid(row=5, column=1)

            self.clear_entries()
            self.root.after(2000, success_label.grid_forget)  # Remove the label after 2 seconds.

    def clear_entries(self) -> None:
        for entry in self.root.winfo_children():
            if isinstance(entry, Entry): entry.delete(0, "end")
