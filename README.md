<p align="center">
  <img src="https://github.com/markod0925/ClipAI/blob/main/images/ClipAI_logo.png" width="18%" />
</p>

# ClipAI

**ClipAI** is a simple but powerful utility to connect your **clipboard** 📋 directly to a **Local LLM** 🤖 (Ollama-based) such as **Gemma 3**, **Phi 4**, **Deepseek-V3**, **Qwen**, **Llama 3.x**, etc. It is a **clipboard viewer** and **text transformer** application built using **Python**. 

It allows users to:
- View the current clipboard content 👀  
- Clear it ❌  
- Modify it ✍️  
- Send it to a language model for text transformations ✨ such as:
  - Rephrasing 🔄  
  - Translating into English 🌐  
  - Summarizing 📑  

It is your **daily companion** for any **writing-related job** ✏️📄. Easy peasy.

The **PC requirements** 🖥️ are mostly related to your preferred LLM, but consider that **Gemma 3-1B-it-qat-q4_0** runs smoothly on a **potato PC** 🥔 (8GB RAM and internal GPU).

## Screenshots

<p align="center">
  <img src="https://github.com/markod0925/ClipAI/raw/main/images/ClipAI_screenshot.PNG" width="60%" />
</p>
<p align="center">
  <img src="https://github.com/markod0925/ClipAI/raw/main/images/ClipAI_screenshot_2.PNG" width="60%" />
</p>

## Features

- **Fully local, all the privacy you need for your data**
- View current clipboard content
- Edit directly in the clipboard textbox the input content
- Clear contents
- Auto-refresh clipboard content
- Send clipboard content to a language model (thanks to Ollama API)
- Select different prompts (e.g., Chat Mode, Rephrase, Translate, Summarization)
- Choose from available language models

## Dependencies

- Python 3.x
- Ollama
- pyperclip
- requests

## Installation

1. Install Ollama:
   Follow the instructions on the [Ollama website](https://ollama.com) to install the Ollama API.

2. Clone the repository:
   ```sh
   git clone https://github.com/markod0925/ClipAI.git
   cd ClipAI
   ```

3. Make an environment and install the required dependencies:
   ```sh
   python -m venv clipAIenv
   .\clipAIenv\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```sh
   python ClipAI.py
   ```

2. The main window will display the current clipboard content. You can use the buttons to refresh, clear, or send the content to a language model.

3. Select the desired transformation type and model from the dropdown menus before sending the content.

## UI Customization and Themes

ClipAI uses the 'clam' theme for a modern look. You can customize the UI by modifying the theme settings in the `ClipAI.py` file. The application uses the `ttk.Style` class to apply the theme and style the widgets. You can refer to the [Tkinter documentation](https://docs.python.org/3/library/tkinter.ttk.html#styling) for more information on how to customize the appearance of the widgets.

## Adding New Prompts

The `prompts.json` is used to store the different prompts that can be applied to the clipboard content. Each key in the dictionary represents the prompt name, and the corresponding value is the prompt template.

### Step-by-Step Guide to Add New Prompts

1. Open the `prompts.json` file in your preferred code editor.
2. Add a new key-value pair to the dictionary, where the key is the name of the prompt, and the value is the prompt template.
3. Run `python ClipAI.py`

### Example

To add a new prompt for rewriting the text in short sentences, you can modify the `prompts.json` file as follows:

```python
{
    "Chat Mode": "\"{}\"",
    "Rephrase": "Please rephrase the following text while keeping the original meaning without any preamble: \"{}\"",
    "Translate in English": "Please translate the following text into English without any preamble: \"{}\"",
    "Summarize": "Please summarize the following text: \"{}\"",
    "Rephrase in short sentences": "Please rephrase the following text in short sentences while keeping the original meaning without any preamble: \"{}\""
}
```

After adding the new prompt, you can select "Rephrase in short sentences" from the dropdown menu in the application to apply the new text transformation to the clipboard content.
