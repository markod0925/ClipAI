import tkinter as tk
from tkinter import messagebox
from src.core import config
from src.ui.clipboard_viewer import ClipboardViewer

def main():
    try:
        # Load configurations
        config.load_configs()
        
        # Create and run the main window
        root = tk.Tk()
        app = ClipboardViewer(root)
        root.mainloop()
    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main() 