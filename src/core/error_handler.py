import tkinter.messagebox as messagebox
from typing import Optional, Callable

class ErrorHandler:
    @staticmethod
    def handle_error(error: Exception, title: str = "Error", show_message_box: bool = True) -> None:
        """Handle an error by logging it and optionally showing a message box"""
        error_message = str(error)
        
        # Log the error (you can add proper logging here)
        print(f"Error: {error_message}")
        
        if show_message_box:
            messagebox.showerror(title, error_message)
    
    @staticmethod
    def safe_execute(func: Callable, error_title: str = "Error", show_message_box: bool = True) -> Optional[any]:
        """Execute a function safely with error handling"""
        try:
            return func()
        except Exception as e:
            ErrorHandler.handle_error(e, error_title, show_message_box)
            return None

class ClipboardError(Exception):
    """Base class for clipboard-related errors"""
    pass

class LLMError(Exception):
    """Base class for LLM-related errors"""
    pass

class ConfigError(Exception):
    """Base class for configuration-related errors"""
    pass 