# ClipAI

<p align="center">
  <img src="https://github.com/markod0925/ClipAI/blob/main/images/ClipAI_logo.png" width="18%" />
</p>

ClipAI is a clipboard viewer and text transformer application built using Tkinter. It allows users to view the current clipboard content, clear it, modify it, and send it to a language model for text transformations such as rephrasing or translating into English or summarizing.

## Screenshots

<p align="center">
  <img src="https://github.com/markod0925/ClipAI/raw/main/images/ClipAI_screenshot.PNG" width="60%" />
</p>
<p align="center">
  <img src="https://github.com/markod0925/ClipAI/raw/main/images/ClipAI_screenshot_2.PNG" width="60%" />
</p>

## Features

- View current clipboard content
- Edit directly in the clipboard textbox the input content
- Clear contents
- Auto-refresh clipboard content
- Send clipboard content to a language model
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
