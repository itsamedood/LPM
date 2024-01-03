from tkinter import Tk, Frame


class BaseFrame(Frame):
  def __init__(self, master: Tk) -> None:
    super().__init__(master)

  def build_frame(self) -> Frame: ...  # Replace with widgets.
