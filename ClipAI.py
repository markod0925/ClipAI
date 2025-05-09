import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyperclip
import threading
import time
import requests
import json
import os

ollamaURL = "http://localhost:11434/api/"
defaultModel = "aya-expanse:latest"

transformationPrompts = None

def core():
    root = tk.Tk()
    app = ClipboardViewer(root)
    root.mainloop()


def main():

    global transformationPrompts
    global ollamaURL
    global defaultModel

    if os.path.isfile('prompts.json'):
        with open("prompts.json", "r", encoding="utf-8") as file:
            transformationPrompts = json.load(file)
            startCore = True
    else:
        show_popup("ERROR: The prompt container file prompts.json does not exist. Please download it from the repo.", "Loading file error")
        startCore = False

    if os.path.isfile('config.json'):
        with open("config.json", "r", encoding="utf-8") as file:
            CONFIGS_DATA = json.load(file)
            ollamaURL = CONFIGS_DATA["OLLAMA_URL"]
            defaultModel = CONFIGS_DATA["DEFAULT_MODEL"]
            startCore = True
    else:
        show_popup("WARNING: The configuration file config.json does not exist. Please download it from the repo for better use. Default parameters will be loaded.", "Loading file error")
        startCore = True

    if startCore:
        core()


def show_popup(message, title="Message"):
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Show the message box
    messagebox.showinfo(title, message)

    # Close the root window after message is shown
    root.destroy()


class ClipboardViewer:
    def __init__(self, root):

        self.root = root

        # Configure the window
        self.root.title("ClipAI")
        self.root.geometry("700x608")
        self.root.minsize(700, 608)
        self.root.resizable(False, False)

        # Load a PNG image
        icon = tk.PhotoImage(file = r'images/ClipAI_icon.png')

        # Set it as window icon
        self.root.iconphoto(True, icon)

        # self.root.wm_attributes("-alpha", 0.95)

        # Apply a theme for improved styling
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Using 'clam' theme for a modern look

        # Create main container with padding
        container = ttk.Frame(self.root, padding=(10, 10))
        container.pack(fill=tk.BOTH)

        # Create a label
        label = ttk.Label(container, text="Clipboard Content:", anchor="w")
        label.pack(fill=tk.X, pady=(0, 5))

        # Create a scrolled text widget for input
        self.text_box = scrolledtext.ScrolledText(
            container,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            height = 11
        )
        self.text_box.pack(fill=tk.X, pady=(0, 5))

        # Create a scrolled text widget for LLM output
        self.out_text_box = scrolledtext.ScrolledText(
            container,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            height = 17,
            bg="#f0f5ff"
        )
        self.out_text_box.pack(fill=tk.X)

        # Make the text box read-only
        self.out_text_box.configure(state="disabled")

        # Create bottom frame for buttons and model selection
        self.button_frame = ttk.Frame(container, height=30)
        self.button_frame.pack(fill=tk.X, pady=(10, 0))

        # Add refresh button
        imageRefresh = tk.PhotoImage(file = r'images/iconRefresh.png')
        self.refresh_button = ttk.Button(
            self.button_frame,
            image=imageRefresh,
            command=self.update_clipboard_content,
            width=12
        )
        self.refresh_button.image = imageRefresh
        self.refresh_button.grid(row=0, column=0, padx=2)

        # Add AUTO-refresh button
        self.imageAutoRefreshOFF = tk.PhotoImage(file = r'images/iconToggleRefresh.png')
        self.imageAutoRefreshON = tk.PhotoImage(file = r'images/iconToggleRefreshON.png')
        self.auto_refresh = False
        self.auto_refresh_button = ttk.Button(
            self.button_frame,
            image=self.imageAutoRefreshOFF,
            command=self.toggle_auto_refresh,
            width=15
        )
        self.auto_refresh_button.grid(row=0, column=1, padx=2)

        # Add clear button
        imageClear = tk.PhotoImage(file = r'images/iconClear.png')
        self.clear_button = ttk.Button(
            self.button_frame,
            image=imageClear,
            command=self.clear_content,
            width=12
        )
        self.clear_button.image = imageClear
        self.clear_button.grid(row=0, column=2, padx=2)

        # Dropdown menu for selecting transformation type
        self.transformation_options = list(transformationPrompts.keys())
        self.selected_transformation = tk.StringVar()
        self.selected_transformation.set(self.transformation_options[0])
        self.transformation_menu = ttk.Combobox(
            self.button_frame,
            textvariable=self.selected_transformation,
            values=self.transformation_options,
            state="readonly",
            width=35
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
        defaultModelLocal = defaultModel
        if defaultModelLocal not in self.model_list:
            defaultModelLocal = self.model_list[0]

        self.selected_model = tk.StringVar(value=defaultModelLocal)
        self.model_menu = ttk.Combobox(
            self.button_frame,
            textvariable=self.selected_model,
            values=self.model_list,
            state="readonly",
            width=30
        )
        self.model_menu.grid(row=0, column=4, padx=5)

        # Send button
        self.imageSend = tk.PhotoImage(file=r'images/iconSend.png')
        self.imageStop = tk.PhotoImage(file=r'images/iconStop.png')

        self.send_button = ttk.Button(
            self.button_frame,
            image=self.imageSend,
            command=self.handle_send_click,
            width=15
        )
        self.send_button.config(image=self.imageSend)
        self.send_button.image = self.imageSend
        self.llm_active = False
        self.llm_response = None
        self.send_button.grid(row=0, column=5, padx=2)

        # Configure grid columns
        for i in range(6):
            self.button_frame.columnconfigure(i, weight=0)
        self.button_frame.columnconfigure(3, weight=1)
        self.button_frame.columnconfigure(4, weight=1)

        # Initialize with current clipboard content
        self.update_clipboard_content()


    def handle_send_click(self):
        if self.llm_active and self.llm_response:
            self.llm_active = False
            self.status_var.set("LLM response stopped by user.")
            self.llm_response.close()
            return
        self.start_qa_llm()


    def fetch_models(self):
        """Fetch available models from Ollama API"""
        try:
            response = requests.get(ollamaURL + "tags")
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
            self.text_box.delete(1.0, tk.END)
            if clipboard_text:
                self.text_box.insert(tk.END, clipboard_text)
                self.status_var.set(f"Updated: {time.strftime('%H:%M:%S')}")
            else:
                self.text_box.insert(tk.END, "Clipboard is empty or contains non-text content.")
                self.status_var.set("No text in clipboard")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")


    def clear_content(self):
        """Clear the text box"""
        self.text_box.delete(1.0, tk.END)
        self.clear_outbox()
        self.status_var.set("Cleared")


    def toggle_auto_refresh(self):
        """Toggle automatic clipboard monitoring"""
        self.auto_refresh = not self.auto_refresh

        if self.auto_refresh:
            self.auto_refresh_button.config(image = self.imageAutoRefreshON)
            self.status_var.set("Auto-refresh enabled")
            self.monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
            self.monitor_thread.start()
        else:
            self.auto_refresh_button.config(image = self.imageAutoRefreshOFF)
            self.status_var.set("Auto-refresh disabled")
            self.monitor_thread = None


    def monitor_clipboard(self):
        """Continuously monitor clipboard for changes"""
        last_content = self.text_box.get('1.0', tk.END)

        while self.auto_refresh:
            current_content = pyperclip.paste()

            if current_content != last_content:
                last_content = current_content
                # Schedule update on the main thread
                self.root.after(0, self.update_clipboard_content)

            time.sleep(0.5)  # Check every half second

    def send_to_llm(self):        

        """Send clipboard text to an Ollama LLM model"""
        clipboard_text = self.text_box.get('1.0', tk.END)
        if not clipboard_text.strip():
            self.status_var.set("Clipboard is empty")
            return

        selected_option = self.selected_transformation.get()
        prompt_template = transformationPrompts.get(selected_option, "{}")
        formatted_prompt = prompt_template.format(clipboard_text)

        model = self.selected_model.get()
        self.status_var.set(f"Sending to {model}...")
        self.root.update_idletasks()

        try:
            response = requests.post(
                ollamaURL + "generate",
                json = {"model": model, "prompt": formatted_prompt, "keep_alive": "5m", "stream": True},
                stream = True
            )

            self.llm_active = True
            self.llm_response = response
            self.send_button.config(image=self.imageStop)
            self.send_button.image = self.imageStop

            if response.status_code == 200:
                self.out_text_box.delete(1.0, tk.END)
                for line in response.iter_lines():
                    if not self.llm_active:
                        break
                    if line:
                        data =  json.loads(line.decode())
                        token = data.get("response", "")
                        self.out_text_box.configure(state="normal")
                        self.out_text_box.insert(tk.END, f"{token}")
                        self.out_text_box.configure(state="disabled")
                        self.out_text_box.see(tk.END)
                        self.root.update_idletasks()
                        
                        # Stop if we detect the end token
                        if data.get("done", False):
                            break                
                self.status_var.set(f"Response received from {model}")
            else:
                self.status_var.set(f"Error {response.status_code}: LLM request failed for {model}")
        except Exception as e:
            if self.llm_active:
                self.status_var.set(f"Error: {str(e)}")
        finally:
            self.llm_response = None
            self.send_button.config(image=self.imageSend)
            self.send_button.image = self.imageSend            


    def start_qa_llm(self):
        self.clear_outbox()
        thread = threading.Thread(target=self.send_to_llm, daemon=True)
        thread.start()


    def clear_outbox(self):
        self.out_text_box.configure(state="normal")
        self.out_text_box.delete(1.0, tk.END)
        self.out_text_box.configure(state="disabled")


if __name__ == "__main__":
    main()
