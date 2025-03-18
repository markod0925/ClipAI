import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import pyperclip
import threading
import time
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_URL_MODEL_LIST = "http://localhost:11434/api/tags"  # API endpoint to get models list
DEFAULT_MODEL = "aya-expanse:latest"

TRANSFORMATION_PROMPTS = {
    "Rephrase": "Please rephrase the following text while keeping the original meaning: \"{}\"",
    "Translate in English": "Please translate the following text into English: \"{}\""
}

class ClipboardViewer:
    def __init__(self, root):
        self.root = root

        # Configure the window
        self.root.title("ClipAI")
        self.root.geometry("700x600")
        self.root.minsize(700, 600)

        # Apply a theme for improved styling
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Using 'clam' theme for a modern look

        # Create main container with padding
        container = ttk.Frame(self.root, padding=(10, 10))
        container.pack(fill=tk.BOTH, expand=True)

        # Create top frame for label
        top_frame = ttk.Frame(container)
        top_frame.pack(fill=tk.X)

        # Create a label
        label = ttk.Label(top_frame, text="Clipboard Content:", anchor="w")
        label.pack(fill=tk.X, pady=(0, 5))

        # Create middle frame for text box
        middle_frame = ttk.Frame(container)
        middle_frame.pack(fill=tk.BOTH, expand=True)

        # Create a scrolled text widget
        self.text_box = scrolledtext.ScrolledText(
            middle_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 10)
        )
        self.text_box.pack(fill=tk.BOTH, expand=True)

        # Make the text box read-only
        self.text_box.configure(state="disabled")

        # Create bottom frame for buttons and model selection
        self.button_frame = ttk.Frame(container, height=30)
        self.button_frame.pack(fill=tk.X, pady=(10, 0))

        # Add refresh button
        self.refresh_button = ttk.Button(
            self.button_frame,
            text="Refresh",
            command=self.update_clipboard_content,
            width=12
        )
        self.refresh_button.grid(row=0, column=0, padx=5)

        self.auto_refresh = False
        self.auto_refresh_button = ttk.Button(
            self.button_frame,
            text="AutoFresh: OFF",
            command=self.toggle_auto_refresh,
            width=15
        )
        self.auto_refresh_button.grid(row=0, column=1, padx=5)

        # Add clear button
        self.clear_button = ttk.Button(
            self.button_frame,
            text="Clear",
            command=self.clear_content,
            width=12
        )
        self.clear_button.grid(row=0, column=2, padx=5)

        # Dropdown menu for selecting transformation type
        self.transformation_options = list(TRANSFORMATION_PROMPTS.keys())
        self.selected_transformation = tk.StringVar()
        self.selected_transformation.set(self.transformation_options[0])
        self.transformation_menu = ttk.Combobox(
            self.button_frame,
            textvariable=self.selected_transformation,
            values=self.transformation_options,
            state="readonly",
            width=18
        )
        self.transformation_menu.grid(row=0, column=3, padx=5)

        # Status bar at the very bottom of main window
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Fetch and set the model list in a dropdown menu
        self.model_list = []
        self.fetch_models()
        defaultModel = DEFAULT_MODEL
        if defaultModel not in self.model_list:
            defaultModel = self.model_list[0]

        self.selected_model = tk.StringVar(value=defaultModel)
        self.model_menu = ttk.Combobox(
            self.button_frame,
            textvariable=self.selected_model,
            values=self.model_list,
            state="readonly",
            width=18
        )
        self.model_menu.grid(row=0, column=4, padx=5)

        # Send button
        self.send_button = ttk.Button(
            self.button_frame,
            text="Send to LLM",
            command=self.send_to_llm,
            width=15
        )
        self.send_button.grid(row=0, column=5, padx=5)

        # Configure grid columns
        for i in range(6):
            self.button_frame.columnconfigure(i, weight=1)

        # Initialize with current clipboard content
        self.update_clipboard_content()

        # Add a class variable to store the LLM response
        self.llm_response = "Chronometer2849"

    def fetch_models(self):
        """Fetch available models from Ollama API"""
        try:
            response = requests.get(OLLAMA_URL_MODEL_LIST)
            response_tmp = response.json()
            # print(response_tmp['models'])
            if response.status_code == 200:
                self.model_list = [model['name'] for model in response_tmp['models']]
                self.model_list = [model for model in self.model_list if "embed" not in model]
                self.model_menu.config(values=self.model_list)
            else:
                self.status_var.set(f"Failed to fetch models: {response.status_code}")
        except Exception as e:
            self.status_var.set(f"Error fetching models: {str(e)}")

    def update_clipboard_content(self):
        """Update the text box with current clipboard content"""
        try:
            clipboard_text = pyperclip.paste()
            self.text_box.configure(state="normal")
            self.text_box.delete(1.0, tk.END)
            if clipboard_text:
                self.text_box.insert(tk.END, clipboard_text)
                self.status_var.set(f"Updated: {time.strftime('%H:%M:%S')}")
            else:
                self.text_box.insert(tk.END, "Clipboard is empty or contains non-text content.")
                self.status_var.set("No text in clipboard")
            self.text_box.configure(state="disabled")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

    def clear_content(self):
        """Clear the text box"""
        self.text_box.configure(state="normal")
        self.text_box.delete(1.0, tk.END)
        self.text_box.configure(state="disabled")
        self.status_var.set("Cleared")

    def toggle_auto_refresh(self):
        """Toggle automatic clipboard monitoring"""
        self.auto_refresh = not self.auto_refresh

        if self.auto_refresh:
            self.auto_refresh_button.config(text="AutoFresh: ON")
            self.status_var.set("Auto-refresh enabled")
            self.monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
            self.monitor_thread.start()
        else:
            self.auto_refresh_button.config(text="AutoFresh: OFF")
            self.status_var.set("Auto-refresh disabled")
            self.monitor_thread = None

    def monitor_clipboard(self):
        """Continuously monitor clipboard for changes"""
        last_content = pyperclip.paste()

        while self.auto_refresh:
            current_content = pyperclip.paste()

            if current_content != last_content and self.llm_response not in current_content:
                last_content = current_content
                # Schedule update on the main thread
                self.root.after(0, self.update_clipboard_content)

            time.sleep(0.5)  # Check every half second

    def send_to_llm(self):
        """Send clipboard text to an Ollama LLM model"""
        clipboard_text = pyperclip.paste()
        if not clipboard_text.strip():
            self.status_var.set("Clipboard is empty")
            return

        selected_option = self.selected_transformation.get()
        prompt_template = TRANSFORMATION_PROMPTS.get(selected_option, "{}")
        formatted_prompt = prompt_template.format(clipboard_text)

        model = self.selected_model.get()

        self.status_var.set(f"Sending to {model}...")

        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": model, "prompt": formatted_prompt, "keep_alive": "5m", "stream": False}
            )

            if response.status_code == 200:
                result = response.json().get("response", "No response from LLM")
                self.text_box.configure(state="normal")
                self.text_box.insert(tk.END, f"\n\nLLM Response:\n{result}")
                self.text_box.configure(state="disabled")
                self.status_var.set(f"Response received from {model}")
                # Store the LLM response in the class variable
                self.llm_response = result
            else:
                self.status_var.set(f"Error {response.status_code}: LLM request failed for {model}")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = ClipboardViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
