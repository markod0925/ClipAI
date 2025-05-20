import tkinter as tk
from tkinter import ttk
import pyperclip
import threading
import time
import json
from src.core import config
from src.core.llm_client import LLMClient
from src.core.markdown_parser import CustomMarkdownParser
from src.core.error_handler import ErrorHandler, ClipboardError, LLMError
from src.ui.components import TextBox, Button, Dropdown, StatusBar

class ClipboardViewer:
    """
    A clipboard viewer and text transformer application that connects to a local LLM.
    
    This class provides a graphical user interface for:
    - Viewing and managing clipboard content
    - Transforming text using local language models
    - Displaying formatted markdown content
    - Managing different transformation types and models
    
    Attributes:
        root (tk.Tk): The main application window
        llm_active (bool): Whether an LLM request is currently active
        llm_response: The current LLM response stream
        current_content (str): The current content being displayed
        is_formatted_view (bool): Whether the content is in formatted view
        markdown_parser (CustomMarkdownParser): Parser for markdown formatting
    """
    
    def __init__(self, root):
        """Initialize the ClipboardViewer."""
        self.root = root
        self.setup_ui()
        self.llm_active = False
        self.llm_response = None
        self.current_content = ""
        self.is_formatted_view = False
        self.markdown_parser = CustomMarkdownParser()

    def setup_ui(self):
        """Initialize and setup all UI components"""
        # Configure the window
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(config.WINDOW_SIZE)
        self.root.minsize(*config.WINDOW_MIN_SIZE)
        self.root.resizable(False, False)

        # Load icon
        icon = tk.PhotoImage(file=config.ICON_PATH)
        self.root.iconphoto(True, icon)

        # Apply theme
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.setup_main_container()
        self.setup_input_area()
        self.setup_output_area()
        self.setup_button_bar()
        self.setup_status_bar()

        # Initialize with current clipboard content
        self.update_clipboard_content()

    def setup_main_container(self):
        """Setup the main container frame"""
        self.container = ttk.Frame(self.root, padding=config.WINDOW_PADDING)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Configure container grid
        self.container.grid_rowconfigure(1, weight=0)  # Input text box row
        self.container.grid_rowconfigure(2, weight=1)  # Output text box row - let it expand
        self.container.grid_columnconfigure(0, weight=1)

    def setup_input_area(self):
        """Setup the input area with label and text box"""
        # Create label
        label = ttk.Label(self.container, text="Clipboard Content:", anchor="w")
        label.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # Create input frame
        input_frame = ttk.Frame(self.container)
        input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        input_frame.grid_columnconfigure(0, weight=1)

        # Create text box
        self.text_box = TextBox(
            input_frame,
            background=config.TEXT_BACKGROUND,
            height=config.NUM_LINES
        )
        self.text_box.grid(row=0, column=0, sticky="ew")

        # Bind Shift+Enter to send_to_llm and prevent default behavior
        def handle_shift_return(event):
            self.handle_send_click()
            return "break"
        self.text_box.bind('<Shift-Return>', handle_shift_return)

    def setup_output_area(self):
        """Setup the output area with text widget"""
        # Create output frame
        output_frame = ttk.Frame(self.container)
        output_frame.grid(row=2, column=0, sticky="nsew")
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        # Calculate dimensions
        font_height = config.FONT_HEIGHT_MULTIPLIER * config.FONT_SIZE
        exact_height = (font_height * config.NUM_LINES)

        # Create text widget
        self.out_text_box = TextBox(
            output_frame,
            background=config.BACKGROUND_COLOR,
            height=config.NUM_LINES
        )
        self.out_text_box.widget.configure(height=exact_height)
        self.out_text_box.grid(row=0, column=0, sticky="nsew")

        # Configure tags
        self.out_text_box.widget.tag_configure('bold', font=(config.FONT_FAMILY, config.FONT_SIZE, "bold"))
        self.out_text_box.widget.tag_configure('italic', font=(config.FONT_FAMILY, config.FONT_SIZE, "italic"))
        self.out_text_box.widget.tag_configure('bold_italic', font=(config.FONT_FAMILY, config.FONT_SIZE, "bold italic"))
        self.out_text_box.widget.tag_configure('heading1', font=(config.FONT_FAMILY, config.FONT_SIZE + 8, "bold"))
        self.out_text_box.widget.tag_configure('heading2', font=(config.FONT_FAMILY, config.FONT_SIZE + 6, "bold"))
        self.out_text_box.widget.tag_configure('heading3', font=(config.FONT_FAMILY, config.FONT_SIZE + 4, "bold"))
        self.out_text_box.widget.tag_configure('heading4', font=(config.FONT_FAMILY, config.FONT_SIZE + 2, "bold"))
        self.out_text_box.widget.tag_configure('heading5', font=(config.FONT_FAMILY, config.FONT_SIZE + 1, "bold"))
        self.out_text_box.widget.tag_configure('heading6', font=(config.FONT_FAMILY, config.FONT_SIZE, "bold"))
        self.out_text_box.widget.tag_configure('bullet', 
            lmargin1=config.BULLET_MARGIN_LEFT, 
            lmargin2=config.BULLET_MARGIN_RIGHT, 
            spacing1=config.BULLET_SPACING, 
            spacing3=config.BULLET_SPACING
        )

        # Bind right-click event to toggle formatting
        self.out_text_box.bind('<Button-3>', self.toggle_output_view)

    def setup_button_bar(self):
        """Setup the button bar with all controls"""
        self.button_frame = ttk.Frame(self.container)
        self.button_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        # Configure button frame grid
        self.button_frame.grid_columnconfigure(3, weight=2)
        self.button_frame.grid_columnconfigure(4, weight=1)
        self.button_frame.grid_columnconfigure(5, weight=0)
        self.button_frame.grid_columnconfigure(6, weight=0)

        # Add buttons
        self.setup_action_buttons()
        self.setup_dropdowns()

    def setup_action_buttons(self):
        """Setup the action buttons (refresh, auto-refresh, clear, copy, send)"""
        # Refresh button
        self.refresh_button = Button(
            self.button_frame,
            config.REFRESH_ICON,
            self.update_clipboard_content,
            config.BUTTON_WIDTH_SMALL
        )
        self.refresh_button.grid(row=0, column=0, padx=2)

        # Auto-refresh button
        self.auto_refresh = False
        self.auto_refresh_off_image = tk.PhotoImage(file=config.AUTO_REFRESH_OFF_ICON)
        self.auto_refresh_on_image = tk.PhotoImage(file=config.AUTO_REFRESH_ON_ICON)
        self.auto_refresh_button = ttk.Button(
            self.button_frame,
            image=self.auto_refresh_off_image,
            command=self.toggle_auto_refresh,
            width=config.BUTTON_WIDTH_MEDIUM
        )
        self.auto_refresh_button.image = self.auto_refresh_off_image  # Keep reference
        self.auto_refresh_button.grid(row=0, column=1, padx=2)

        # Clear button
        self.clear_button = Button(
            self.button_frame,
            config.CLEAR_ICON,
            self.clear_content,
            config.BUTTON_WIDTH_SMALL
        )
        self.clear_button.grid(row=0, column=2, padx=2)

        # Copy button
        self.copy_button = Button(
            self.button_frame,
            config.COPY_ICON,
            self.copy_output_content,
            config.BUTTON_WIDTH_SMALL
        )
        self.copy_button.grid(row=0, column=6, padx=2)

        # Send button
        self.send_image = tk.PhotoImage(file=config.SEND_ICON)
        self.stop_image = tk.PhotoImage(file=config.STOP_ICON)
        self.send_button = ttk.Button(
            self.button_frame,
            image=self.send_image,
            command=self.handle_send_click,
            width=config.BUTTON_WIDTH_MEDIUM
        )
        self.send_button.image = self.send_image  # Keep reference
        self.send_button.grid(row=0, column=5, padx=2)

    def setup_dropdowns(self):
        """Setup the transformation and model selection dropdowns"""
        # Transformation type dropdown
        self.transformation_options = list(config.TRANSFORMATION_PROMPTS.keys())
        self.transformation_menu = Dropdown(
            self.button_frame,
            self.transformation_options,
            self.transformation_options[0],
            config.TRANSFORMATION_MENU_WIDTH
        )
        self.transformation_menu.grid(row=0, column=3, padx=5, sticky="ew")

        # Model selection dropdown
        self.model_menu = Dropdown(
            self.button_frame,
            [],  # Will be populated by fetch_models
            config.DEFAULT_MODEL,
            config.MODEL_MENU_WIDTH
        )
        self.model_menu.grid(row=0, column=4, padx=5, sticky="ew")
        
        # Initialize model list
        self.model_list = []
        self.fetch_models()

    def setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = StatusBar(self.container)
        self.status_bar.grid(row=4, column=0, sticky="ew", pady=(2, 2))

    def switch_to_html_view(self):
        """Switch from plain text to formatted view"""
        if not self.is_formatted_view and self.current_content:
            try:
                # First clear the text widget
                self.out_text_box.delete(1.0, tk.END)
                
                # Parse the markdown content
                plain_text, tags = self.markdown_parser.parse(self.current_content)
                
                # Insert the plain text
                self.out_text_box.insert(tk.END, plain_text)
                
                # Apply tags in reverse order to handle nested formatting
                for tag_name, start, end in sorted(tags, key=lambda x: x[1], reverse=True):
                    try:
                        # Convert character positions to line.column format
                        start_line = "1.0"
                        end_line = "1.0"
                        
                        # Add the tag
                        self.out_text_box.widget.tag_add(tag_name, f"{start_line}+{start}c", f"{end_line}+{end}c")
                    except Exception as e:
                        ErrorHandler.handle_error(e, "Tag Application Error", show_message_box=False)
                
                self.is_formatted_view = True
            except Exception as e:
                ErrorHandler.handle_error(e, "Formatting Error")

    def switch_to_text_view(self):
        """Switch from formatted to plain text view"""
        if self.is_formatted_view and self.current_content:
            try:
                self.out_text_box.delete(1.0, tk.END)
                self.out_text_box.insert(tk.END, self.current_content)
                self.is_formatted_view = False
            except Exception as e:
                ErrorHandler.handle_error(e, "View Switch Error")

    def handle_send_click(self):
        """Handle send button click"""
        if self.llm_active and self.llm_response:
            self.llm_active = False
            self.status_bar.set(config.STATUS_STOPPED)
            self.llm_response.close()
            return
        self.start_qa_llm()

    def fetch_models(self):
        """Fetch available models from Ollama API"""
        def fetch():
            try:
                self.model_list = LLMClient.fetch_models()
                self.model_menu.config(values=self.model_list)
                if self.model_menu.get() not in self.model_list:
                    self.model_menu.set(self.model_list[0])
            except Exception as e:
                raise LLMError(f"Failed to fetch models: {str(e)}")

        ErrorHandler.safe_execute(fetch, "Model Fetch Error")

    def update_clipboard_content(self):
        """Update the text box with current clipboard content"""
        def update():
            try:
                clipboard_text = pyperclip.paste()
                self.text_box.delete(1.0, tk.END)
                if clipboard_text:
                    self.text_box.insert(tk.END, clipboard_text)
                    self.status_bar.set(config.STATUS_UPDATED.format(time.strftime('%H:%M:%S')))
                else:
                    self.text_box.insert(tk.END, config.STATUS_EMPTY)
                    self.status_bar.set(config.STATUS_NO_TEXT)
            except Exception as e:
                raise ClipboardError(f"Failed to update clipboard: {str(e)}")

        ErrorHandler.safe_execute(update, "Clipboard Update Error")

    def clear_content(self):
        """Clear the text box"""
        try:
            self.text_box.delete(1.0, tk.END)
            self.clear_outbox()
            self.status_bar.set(config.STATUS_CLEARED)
        except Exception as e:
            ErrorHandler.handle_error(e, "Clear Error")

    def clear_outbox(self):
        """Clear the output box"""
        try:
            self.current_content = ""
            self.is_formatted_view = False
            self.out_text_box.delete(1.0, tk.END)
        except Exception as e:
            ErrorHandler.handle_error(e, "Output Clear Error")

    def toggle_auto_refresh(self):
        """Toggle automatic clipboard monitoring"""
        try:
            self.auto_refresh = not self.auto_refresh
            if self.auto_refresh:
                self.auto_refresh_button.configure(image=self.auto_refresh_on_image)
                self.auto_refresh_button.image = self.auto_refresh_on_image  # Keep reference
                self.status_bar.set(config.STATUS_AUTO_REFRESH_ENABLED)
                if self.monitor_thread is None or not self.monitor_thread.is_alive(): 
                    self.monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
                    self.monitor_thread.start()
            else:
                self.auto_refresh_button.configure(image=self.auto_refresh_off_image)
                self.auto_refresh_button.image = self.auto_refresh_off_image  # Keep reference
                self.status_bar.set(config.STATUS_AUTO_REFRESH_DISABLED)
                self.monitor_thread = None
        except Exception as e:
            ErrorHandler.handle_error(e, "Auto-refresh Toggle Error")

    def monitor_clipboard(self):
        """Continuously monitor clipboard for changes"""
        last_content = self.text_box.get('1.0', tk.END)
        while self.auto_refresh:
            try:
                current_content = pyperclip.paste()
                if current_content != last_content:
                    last_content = current_content
                    self.root.after(0, self.update_clipboard_content)
                time.sleep(0.5)
            except Exception as e:
                ErrorHandler.handle_error(e, "Clipboard Monitor Error", show_message_box=False)
                break

    def start_qa_llm(self):
        """Start the LLM query in a separate thread"""
        self.clear_outbox()
        if thread is None or not thread.is_alive():
            thread = threading.Thread(target=self.send_to_llm, daemon=True)
            thread.start()

    def send_to_llm(self):
        """Send clipboard text to an Ollama LLM model"""
        def send():
            clipboard_text = self.text_box.get('1.0', tk.END)
            if not clipboard_text.strip():
                self.status_bar.set(config.STATUS_NO_TEXT)
                return

            selected_option = self.transformation_menu.get()
            prompt_template = config.TRANSFORMATION_PROMPTS.get(selected_option, "{}")
            formatted_prompt = prompt_template.format(clipboard_text)

            model = self.model_menu.get()
            self.status_bar.set(config.STATUS_SENDING.format(model))
            self.root.update_idletasks()

            try:
                self.llm_active = True
                self.llm_response = LLMClient.generate_stream(model, formatted_prompt)
                self.send_button.configure(image=self.stop_image)
                self.send_button.image = self.stop_image  # Keep reference

                self.current_content = ""
                self.is_formatted_view = False
                
                for line in self.llm_response.iter_lines():
                    if not self.llm_active:
                        break
                    if line:
                        data = json.loads(line.decode())
                        token = data.get("response", "")
                        self.current_content += token
                        
                        # Update streaming text
                        self.out_text_box.delete(1.0, tk.END)
                        self.out_text_box.insert(tk.END, self.current_content)
                        self.out_text_box.see(tk.END)
                        self.root.update_idletasks()
                        
                        # If this is the last token, switch to HTML widget with formatting
                        if data.get("done", False):
                            self.switch_to_html_view()
                            break
                self.status_bar.set(config.STATUS_RECEIVED.format(model))
            except Exception as e:
                if self.llm_active:
                    raise LLMError(f"LLM request failed: {str(e)}")
            finally:
                self.llm_response = None
                self.send_button.configure(image=self.send_image)
                self.send_button.image = self.send_image  # Keep reference

        ErrorHandler.safe_execute(send, "LLM Request Error")

    def copy_output_content(self):
        """Copy the content of the output text box to clipboard"""
        def copy():
            content = self.out_text_box.get(1.0, tk.END).strip()
            if content:
                pyperclip.copy(content)
                self.status_bar.set(config.STATUS_COPIED)
            else:
                self.status_bar.set(config.STATUS_NO_CONTENT)

        ErrorHandler.safe_execute(copy, "Copy Error")

    def toggle_output_view(self, event=None):
        """Toggle between formatted and plain text view"""
        try:
            if self.is_formatted_view:
                self.switch_to_text_view()
            else:
                self.switch_to_html_view()
        except Exception as e:
            ErrorHandler.handle_error(e, "View Toggle Error") 
