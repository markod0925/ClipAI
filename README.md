# ClipAI

ClipAI is a clipboard viewer and transformer application built using Tkinter. It allows users to view the current clipboard content, clear it, and send it to a language model for transformations such as rephrasing or translating into English.

## Features

- View current clipboard content
- Clear clipboard content
- Auto-refresh clipboard content
- Send clipboard content to a language model for transformations
- Select different transformation types (e.g., rephrase, translate)
- Choose from available language models

## Dependencies

- Python 3.x
- Tkinter
- pyperclip
- requests
- Ollama

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/markod0925/ClipAI.git
   cd ClipAI
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Install Ollama:
   Follow the instructions on the [Ollama website](https://ollama.com) to install the Ollama API.

## Usage

1. Run the application:
   ```sh
   python ClipAI.py
   ```

2. The main window will display the current clipboard content. You can use the buttons to refresh, clear, or send the content to a language model.

3. Select the desired transformation type and model from the dropdown menus before sending the content.

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
