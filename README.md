# TeleTrans - The Telegram Translator

TeleTrans is a Python-based Telegram bot that translates messages in real-time. It uses the OpenAI API and DeepL API for translation.

## Features

- Real-time translation of messages.
- Supports multiple languages.
- Uses OpenAI and DeepL for translation.
- Configurable source and target languages.
- Command mode for enabling/disabling translation and setting languages.

## Requirements

- Python 3.6+
- aiohttp
- telethon
- requests

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/teletrans.git
   ```
2. Navigate to the project directory:
   ```
   cd teletrans
   ```
3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
4. Create a `config.json` file in the project directory and fill it with your API keys and other configuration details.
    ```json
    {
        "api_id": "your_telegram_api_id",
        "api_hash": "your_telegram_api_hash",
        "target_config": {},
        "openai": {
            "enable": true,
            "api_key": "your_openai_api_key",
            "url": "https://api.openai.com/v1/chat/completions",
            "model": "gpt-3.5-turbo"
        }
    }
    ```

## Usage

1. Run the script with an optional argument to specify the working directory:
   ```
   python teletrans.py </path/to/your/directory>
   ```
   If no directory is specified, the script will run in the current directory.

2. To enable translation from Chinese to English and Japanese, you would use:
   ```
   .tt-on,zh,zh|en|ja
   ```


3. To disable translation, simply use:
   ```
   .tt-off
   ```

4. If you want to send a message without translating it, use the `.tt-skip` command followed by your message:
   ```
   .tt-skip Hello, this message will not be translated.
   ```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

