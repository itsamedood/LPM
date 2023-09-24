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
