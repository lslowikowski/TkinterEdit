import tkinter as tk
class RadioGroup:
    def __init__(self, name):
        self.name = name
        self.var = tk.StringVar()
        self.options = []