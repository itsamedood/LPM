from frames.addNewSet import AddNewSetFrame
from frames.select import SelectFrame
from paths import Paths
from tkinter import Tk, Frame


class GUI:
  def __init__(self) -> None:
    self.paths = Paths()
    self.current_frame = None

    # Create window.
    self.root = Tk()
    self.root.title("LPM - itsamedood")
    self.root.geometry("320x240")
    self.root.resizable(False, False)

    self.build_all_frames()
    self.show_frame(self.select_frame.build_frame())

  def build_all_frames(self) -> None:
    self.select_frame = SelectFrame(self.root, self.paths)
    self.add_new_set_frame = AddNewSetFrame(self.root, self.paths)

  def show_frame(self, _frame: Frame) -> None:
    if self.current_frame is not None:
      self.current_frame.grid_remove()

    _frame.grid()
    _frame.tkraise()
    self.current_frame = _frame

  def run(self) -> None: self.root.mainloop()


# Run.
GUI().run()
