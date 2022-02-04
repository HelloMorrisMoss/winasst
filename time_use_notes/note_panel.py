"""A GUI panel for adding or modifying a time use note."""

import tkinter as tk
from tkinter import ttk
import ttkwidgets


class NotePanel(ttk.Frame):
    def __init__(self, parent: ttk.widget, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._time_var = tk.StringVar()
        self._time_entry = ttk.Entry(self,)
