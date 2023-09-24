from frames.addNewSet import AddNewSet
from paths import Paths
from tkinter import Tk, Frame


class GUI:
    def __init__(self) -> None:
        self.paths = Paths()

        # Create window.
        self.root = Tk()
        self.root.title("LPM - itsamedood")
        self.root.geometry("320x240")
        self.root.resizable(False, False)

        # Build all frames.
        add_new_set_frame = AddNewSet(self.root, self.paths).build_frame()

        self.show_frame(add_new_set_frame)

    def show_frame(self, _frame: Frame) -> None:
        _frame.grid()
        _frame.tkraise()

    def run(self) -> None:
        self.root.mainloop()


# Run.
GUI().run()
