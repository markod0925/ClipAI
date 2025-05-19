import os
import json

# Default configurations
OLLAMA_URL = "http://localhost:11434/api/"
DEFAULT_MODEL = "aya-expanse:latest"
TRANSFORMATION_PROMPTS = None

# Window configuration
WINDOW_TITLE = "ClipAI"
WINDOW_SIZE = "700x608"
WINDOW_MIN_SIZE = (700, 608)
WINDOW_PADDING = (10, 10)

# Font configuration
FONT_FAMILY = "Segoe UI"
FONT_SIZE = 10
FONT_HEIGHT_MULTIPLIER = 1.2
NUM_LINES = 10

# Colors
BACKGROUND_COLOR = "#f0f5ff"
TEXT_BACKGROUND = "white"

# Button sizes
BUTTON_WIDTH_SMALL = 12
BUTTON_WIDTH_MEDIUM = 15

# Dropdown sizes
TRANSFORMATION_MENU_WIDTH = 25
MODEL_MENU_WIDTH = 20

# Margins and spacing
BULLET_MARGIN_LEFT = 20
BULLET_MARGIN_RIGHT = 40
BULLET_SPACING = 2

# File paths
ICON_PATH = 'images/ClipAI_icon.png'
REFRESH_ICON = 'images/iconRefresh.png'
AUTO_REFRESH_OFF_ICON = 'images/iconToggleRefresh.png'
AUTO_REFRESH_ON_ICON = 'images/iconToggleRefreshON.png'
CLEAR_ICON = 'images/iconClear.png'
SEND_ICON = 'images/iconSend.png'
STOP_ICON = 'images/iconStop.png'
COPY_ICON = 'images/iconCopy.png'

# Status messages
STATUS_READY = "Ready"
STATUS_UPDATED = "Updated: {}"
STATUS_EMPTY = "Clipboard is empty or contains non-text content"
STATUS_NO_TEXT = "No text in clipboard"
STATUS_CLEARED = "Cleared"
STATUS_AUTO_REFRESH_ENABLED = "Auto-refresh enabled"
STATUS_AUTO_REFRESH_DISABLED = "Auto-refresh disabled"
STATUS_SENDING = "Sending to {}..."
STATUS_RECEIVED = "Response received from {}"
STATUS_STOPPED = "LLM response stopped by user."
STATUS_COPIED = "Output content copied to clipboard"
STATUS_NO_CONTENT = "No content to copy"

def load_configs():
    global OLLAMA_URL, DEFAULT_MODEL, TRANSFORMATION_PROMPTS
    
    # Load prompts
    if os.path.isfile('prompts.json'):
        with open("prompts.json", "r", encoding="utf-8") as file:
            TRANSFORMATION_PROMPTS = json.load(file)
            start_core = True
    else:
        raise FileNotFoundError("ERROR: The prompt container file prompts.json does not exist. Please download it from the repo.")

    # Load configuration
    if os.path.isfile('config.json'):
        with open("config.json", "r", encoding="utf-8") as file:
            CONFIGS_DATA = json.load(file)
            OLLAMA_URL = CONFIGS_DATA["OLLAMA_URL"]
            DEFAULT_MODEL = CONFIGS_DATA["DEFAULT_MODEL"]
    else:
        print("WARNING: The configuration file config.json does not exist. Using default parameters.") 