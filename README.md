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
   - `api_id` and `api_hash` are required for the Telegram API. You can get them by creating a new application at [my.telegram.org](https://my.telegram.org).
   - If `openai.enable` is set to `true`, the bot will use the OpenAI API to translate, and this is only effective when the target language is English.

## Usage

1. Run the script with an optional argument to specify the working directory:
   ```
   python teletrans.py </path/to/your/directory>
   ```
   If no directory is specified, the script will run in the current directory.

2. To enable translation from Chinese to English and Japanese, and keep the original message, use the following command:
   ```
   .tt-on,zh,zh|en|ja
   ```
   The code of languages supported by DeepL API can be found [here](https://developers.deepl.com/docs/resources/supported-languages).

3. To disable translation, simply use:
   ```
   .tt-off
   ```

4. If you want to send a message without translating it, use the `.tt-skip` command followed by your message:
   ```
   .tt-skip Hello, this message will not be translated.
   ```

5. Edited message is not translated by default. If you need to translate it, insert `.tt` at the beginning of the message.
   ```
   .tt This edited message will be translated.
   ```

## Daemon

1. To run the script as a daemon, you can use systemd. Create a new service file:
   ```
   sudo nano /etc/systemd/system/teletrans.service
   ```

2. Add the following content to the file:
   ```
   [Unit]
   Description=TeleTrans
   After=network.target

   [Service]
   Type=simple
   User=yourusername
   WorkingDirectory=/path/to/teletrans
   ExecStart=/usr/bin/python3 /path/to/teletrans/teletrans.py /path/to/your/directory
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```
   Replace `yourusername` and `/path/to/teletrans` with your username and the path to the project directory. `/path/to/your/directory` is the directory where the bot will store the database and logs.

3. Start the service and enable it to run on boot:
   ```
   sudo systemctl start teletrans
   sudo systemctl enable teletrans
   ```

4. Check the status of the service:
   ```
   sudo systemctl status teletrans
   ```

5. To stop the service, use:
   ```
   sudo systemctl stop teletrans
   ```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MPL-2.0 License - see the [LICENSE](LICENSE) file for details.

