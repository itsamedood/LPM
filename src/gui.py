from tkinter import Tk, Label, Text
# from tkinter.ttk import *

# Create window.
root = Tk()
root.title("LPM - itsamedood")
root.geometry("640x480")

# Create elements.
parent_box = Text(root, height=5, width=25, bg="light yellow")

# Add elements.
parent_box.pack()

# Run.
root.mainloop()
