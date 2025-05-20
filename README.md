<p align="center">
  <img src="https://github.com/markod0925/ClipAI/blob/main/images/ClipAI_logo.png" width="18%" />
</p>

# ClipAI

**ClipAI** is a simple but powerful utility to connect your **clipboard** 📋 directly to a **Local LLM** 🤖 (Ollama-based) such as **Gemma 3**, **Phi 4**, 
**Deepseek-V3**, **Qwen**, **Llama 3.x**, etc. It is a **clipboard viewer** and **text transformer** application built using **Python**. 

It is your **daily companion** for any **writing-related job** ✏️📄. Easy peasy.

The **PC requirements** 🖥️ are mostly related to your preferred LLM, but consider that 
**Gemma 3-1B-it-qat-q4_0** runs smoothly on a **potato PC** 🥔 (8GB RAM and internal GPU).

## Features

- **Real-time Clipboard Monitoring**: Automatically detect and display clipboard content changes
- **Text Transformation**: Transform clipboard content using various AI-powered operations
- **Markdown Support**: output text can be view using markdown styling
- **Multiple LLM Models**: Support for different language models through Ollama
- **Customizable Prompts**: Configure different transformation types through prompts.json
- **Auto-refresh**: Toggle automatic clipboard monitoring
- **Format Toggle**: Switch between plain text and Markdown formatted views
- **Copy Output**: Easily copy transformed content back to clipboard

## Screenshots

<p align="center">
  <img src="https://github.com/markod0925/ClipAI/raw/main/images/ClipAI_screenshot.PNG" width="45%" />
  <img src="https://github.com/markod0925/ClipAI/raw/main/images/ClipAI_screenshot_2.PNG" width="45%" />
</p>

## Requirements

- Python 3.8+
- Ollama running (see [https://ollama.com/](https://ollama.com/) to install Ollama)
- Required Python packages:
  - pyperclip
  - requests
  - pyinstaller (only to build the project by yourself, see below how to do it)

## Usage

1. Copy any text to your clipboard
2. Select desired transformation type
3. Choose LLM model
4. Click Send button or press **Shift+Enter**
5. View transformed output
6. Use right-click to toggle formatting
7. Copy output using the copy button

## Installation

### Option 1 (run Python script)
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure Ollama and ensure it's running
5. Run the application:
   ```bash
   python run.py
   ```

### Option 2 (run executable file, Win Only)
1. Download the zip file from last [Release](https://github.com/markod0925/ClipAI/releases)
2. Extract the files
3. Run the .exe

### Option 3 (build the executable by yourself and run it)
1. Follow the instruction [here](https://github.com/markod0925/ClipAI/tree/CursorTests#building-executables)

## UI Elements

### Buttons

1. **Refresh Button** (![](images/iconRefresh.png))
   - Manually updates the clipboard content
   - Useful when auto-refresh is disabled

2. **Auto-refresh Toggle** (![](images/iconToggleRefresh.png))
   - Toggles automatic clipboard monitoring
   - ![](images/iconToggleRefreshON.png) indicates active monitoring
   - ![](images/iconToggleRefresh.png) indicates manual mode

3. **Clear Button** (![](images/iconClear.png))
   - Clears both input and output text areas
   - Resets the current state

4. **Send Button** (![](images/iconSend.png))
   - Sends content to the selected LLM model
   - Changes to stop icon (![](images/iconStop.png)) during processing
   - Click again to stop the current operation

5. **Copy Button** (![](images/iconCopy.png))
   - Copies the output content to clipboard
   - Only active when there is content to copy


### Dropdowns

1. **Transformation Type**
   - Selects the type of transformation to apply
   - Options are loaded from prompts.json
   - Examples might include:
     - Summarization
     - Translation
     - Code explanation
     - Text formatting
     - Custom transformations

2. **Model Selection**
   - Chooses the LLM model to use
   - Automatically populated from available Ollama models
   - Default model is set in config.json

### Text Areas

1. **Input Area**
   - Displays current clipboard content
   - Updates automatically when auto-refresh is enabled
   - Supports manual updates via refresh button

2. **Output Area**
   - Shows transformed content
   - Supports markdown formatting
   - Right-click to toggle between formatted and plain text views

### Status Bar
- Shows current operation status
- Displays error messages
- Indicates clipboard updates
- Shows LLM operation progress

## Configuration

### config.json
```json
{
    "OLLAMA_URL": "http://localhost:11434/api/",
    "DEFAULT_MODEL": "aya-expanse:latest"
}
```

### prompts.json
Contains transformation templates for different operations. Each template can include:
- Description
- System prompt
- User prompt template
- Example inputs/outputs

## Adding New Prompts

The `prompts.json` is used to store the different prompts that can be applied to the clipboard content. Each key in the dictionary represents the prompt name, and the corresponding value is the prompt template.

### Step-by-Step Guide to Add New Prompts

1. Open the `prompts.json` file in your preferred code editor.
2. Add a new key-value pair to the dictionary, where the key is the name of the prompt, and the value is the prompt template.
3. Run `python run.py`

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

## Building Executables

To build standalone executables for Windows, Linux, or macOS:

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```bash
   python build.py
   ```

The executables will be created in the `dist` directory, organized by platform:
- Windows: `dist/windows/ClipAI.exe`
- Linux: `dist/linux/ClipAI`
- macOS: `dist/darwin/ClipAI`

Each platform directory contains:
- The executable file
- Required configuration files (config.json, prompts.json)
- Images directory with all icons
- README.md

Note: To build for a specific platform, you need to run the build script on that platform. Cross-platform building is not supported.

## Project Structure

```
run.py
build.py
config.json
prompts.json
src/
├── __init__.py
├── main.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── error_handler.py
│   ├── llm_client.py
│   └── markdown_parser.py
└── ui/
    ├── __init__.py
    ├── clipboard_viewer.py
    └── components.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
