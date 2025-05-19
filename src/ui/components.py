import tkinter as tk
from tkinter import ttk, scrolledtext
from src.core import config

class TextBox:
    def __init__(self, parent, **kwargs):
        self.widget = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            font=(config.FONT_FAMILY, config.FONT_SIZE),
            background=kwargs.get('background', config.TEXT_BACKGROUND),
            height=kwargs.get('height', config.NUM_LINES)
        )
        
    def grid(self, **kwargs):
        self.widget.grid(**kwargs)
        
    def delete(self, start, end):
        self.widget.delete(start, end)
        
    def insert(self, index, text):
        self.widget.insert(index, text)
        
    def get(self, start, end):
        return self.widget.get(start, end)
        
    def see(self, index):
        self.widget.see(index)
        
    def bind(self, sequence, func):
        self.widget.bind(sequence, func)

class Button:
    def __init__(self, parent, image_path, command, width):
        self.image = tk.PhotoImage(file=image_path)
        self.widget = ttk.Button(
            parent,
            image=self.image,
            command=command,
            width=width
        )
        self.widget.image = self.image  # Keep reference
        
    def grid(self, **kwargs):
        self.widget.grid(**kwargs)
        
    def config(self, **kwargs):
        self.widget.config(**kwargs)

class Dropdown:
    def __init__(self, parent, values, default_value, width, state="readonly"):
        self.variable = tk.StringVar(value=default_value)
        self.widget = ttk.Combobox(
            parent,
            textvariable=self.variable,
            values=values,
            state=state,
            width=width
        )
        
    def grid(self, **kwargs):
        self.widget.grid(**kwargs)
        
    def get(self):
        return self.variable.get()
        
    def set(self, value):
        self.variable.set(value)
        
    def config(self, **kwargs):
        self.widget.config(**kwargs)

class StatusBar:
    def __init__(self, parent):
        self.variable = tk.StringVar(value=config.STATUS_READY)
        self.widget = ttk.Label(
            parent,
            textvariable=self.variable,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2)
        )
        
    def grid(self, **kwargs):
        self.widget.grid(**kwargs)
        
    def set(self, text):
        self.variable.set(text)
        
    def get(self):
        return self.variable.get() 