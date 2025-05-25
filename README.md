# Character AI Chat Interface

A beautiful command-line interface for interacting with Character AI, featuring ASCII art, colored output, and a user-friendly chat experience.

![Character AI Chat]

## Features

- 🎨 Beautiful ASCII-based UI with colors
- 💬 Interactive chat interface with Character AI
- 🔄 Easy character switching
- 📝 Character management (add/remove characters)
- 🎯 Multiple character support
- 🔒 Secure credential management

## Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/fawzankhan-404/character-Ai404-.git
cd character-ai-chat
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `creds.py` file in the project root with your credentials:
```python
CREDENTIALS = {
    'email': 'your-email@gmail.com',
    'password': 'your-password'
}

DEFAULT_CHARACTERS = {
    'jarvis': 'https://character.ai/chat/1U5b4Nuuf3LnBLvAbaxUfllTYvttzWH2m4hjvj5ubfE',
    'tony stark': 'https://character.ai/chat/pe5AdTpnjL-r_pya0JoXXd1UMlYpiRiQ0bgzcxHJwrg'
}
```

## Usage

### Basic Usage

Start a chat session with a specific character:
```bash
python main.py -n "jarvis"
```

### Available Commands

- `switch` - Change to a different character
- `help` - Show available commands
- `exit` - End the session

### Command Line Options

- `-n, --name` - Specify character name to chat with
- `-l, --list` - List available characters
- `-r, --register` - Register a new character (name and URL)
- `-d, --delete` - Delete a character

Examples:
```bash
# List all characters
python main.py -l

# Register a new character
python main.py -r "character_name" "character_url"

# Delete a character
python main.py -d "character_name"
```

## Character Management

### Adding Characters

1. Find the character's chat URL on Character AI
2. Register the character using the `-r` option:
```bash
python main.py -r "character_name" "https://character.ai/chat/..."
```

### Removing Characters

Delete a character using the `-d` option:
```bash
python main.py -d "character_name"
```

## UI Features

- 🎨 Colored ASCII art logo
- 💬 Chat bubbles for messages
- 🎯 Clear visual distinction between user and AI messages
- 📝 Formatted command list
- ⚡ Real-time response display

## Troubleshooting

1. **Login Issues**
   - Ensure your credentials are correct in `creds.py`
   - Check your internet connection
   - Verify Chrome browser is installed

2. **Character Not Found**
   - Verify the character exists in your character list
   - Check the character URL is valid
   - Use `-l` to list available characters

3. **Response Issues**
   - Check your internet connection
   - Verify the character is online
   - Try switching to a different character

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE] file for details.

## Acknowledgments

- Character AI for providing the chat platform
- Colorama for cross-platform color support
- Selenium for browser automation

## Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue if needed

---

Made with ❤️ by [FawzanKhan] 
