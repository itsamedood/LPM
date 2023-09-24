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
