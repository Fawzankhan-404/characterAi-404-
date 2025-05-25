# Character AI Interaction Script

A Python script for interacting with Character AI via a command-line interface, supporting both text and voice modes.

## Features

*   💬 Interactive chat interface with Character AI
*   🎤 Voice interaction mode for hands-free commands and messaging
*   🗣 Text-to-speech for AI responses (optional)
*   🔄 Ability to select a character via command line argument
*   🎯 Multiple character support (pre-defined in the script)
*   📞 In-chat commands for initiating and ending calls
*   📝 Command line arguments for controlling script behavior (chat mode, voice mode, list characters, specify character)

## Prerequisites

*   Python 3.7 or higher
*   Chrome browser installed
*   Internet connection
*   `pyaudio` for voice input (may require additional system dependencies)

## Installation

1.  Clone the repository (or download the `character_ai.py` and `requirements.txt` files).
2.  Navigate to the project directory.
3.  Create and activate a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4.  Install required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

*   Character URLs are hardcoded in the `CHARACTER_URLS` dictionary within the `character_ai.py` file.
*   Login credentials (`your@gmail.com` and `yourpass`) are hardcoded in the `login` method within `character_ai.py`. **It is highly recommended to use a fake account or which dosent have your personal info.**

## Usage

Run the script from your terminal. By default, it runs in voice mode.

```bash
python character_ai.py
```

### Command Line Options

*   `-c, --chat`: Run in chat mode (text-based interaction).
*   `-n, --name`: Specify character name to chat with directly.
*   `-l, --list`: List available characters.
*   `-s, --speak`: Enable text-to-speech for AI responses.

Examples:

```bash
# Run in chat mode with Jarvis
python character_ai.py --chat --name "jarvis"

# List available characters
python character_ai.py --list

# Run in voice mode with text-to-speech enabled
python character_ai.py --speak
```

### In-Chat Commands (Chat Mode)

*   `exit`, `quit`, `stop`: End the session.
*   `switch character` or `switch ch`: Change to a different character.
*   `call` or `start call`: Initiate a call (if available for the character).
*   `hang up`, `hangup`, `cut`, `end call`: End a call.

### Voice Commands (Voice Mode)

*   `call` or `start call`: Initiate a call (if available for the character).
*   `hang up`, `hangup`, `cut`, `end call`: End a call.
*   `stop listening` or `stop voice`: Stop voice command listening.
*   Any other speech will be sent as a message to the character.

## Troubleshooting

1.  **Login Issues**
    *   Ensure your internet connection is stable.
    *   Verify Chrome browser is installed.
    *   Check if Character AI requires manual login or verification outside the script's automated process.
2.  **Character Not Found**
    *   Verify the character name is spelled correctly and exists in the `CHARACTER_URLS` dictionary.
    *   Use the `--list` option to see available characters.
3.  **Response Issues / Timouts**
    *   Check your internet connection.
    *   The script relies on finding specific elements in the browser; changes to the Character AI website layout may break functionality.
4.  **Voice Recognition Issues**
    *   Ensure your microphone is working and selected correctly in your system settings.
    *   Check for `pyaudio` installation issues.
    *   Background noise can affect recognition; try a quieter environment.
5.  **Text-to-Speech Issues**
    *   Ensure `pyttsx3` is installed correctly.
    *   Check your system's audio output.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE] file for details.

## Acknowledgments

*   Character AI for providing the chat platform
*   Selenium for browser automation
*   SpeechRecognition for voice input
*   pyttsx3 for text-to-speech

## Support

If you encounter any issues or have questions, please:

1.  Check the troubleshooting section.
2.  Create a new issue on the GitHub repository if applicable.

---

Made with ❤️ by [FawzanKhan] 
