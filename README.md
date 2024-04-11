# TeleTrans - The Telegram Translator

TeleTrans is a Python-based Telegram bot that translates messages in real-time. It uses the OpenAI API and DeepL API for translation.

## Features

- Real-time translation of messages.
- Supports multiple languages.
- Uses OpenAI and DeepL for translation.
- Configurable source and target languages.
- Command mode for enabling/disabling translation and setting languages.

## Requirements

- Python 3.10+
- aiohttp
- telethon
- requests

## Manual Installation

<details>
   <summary>Click for manual install details</summary>

#### Install & Setup & Run

1. Clone the repository:
   ```sh
   git clone https://github.com/ihategfw/teletrans.git
   ```
2. Navigate to the project directory:
   ```sh
   cd teletrans
   ```
3. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `config.json` file in the project directory:
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

5. Run the script with an optional argument to specify the working directory:
   ```sh
   python teletrans.py </path/to/your/directory>
   ```
   If no directory is specified, the script will run in the current directory.

#### Running as a Daemon

1. Create a new service file:
   ```sh
   sudo nano /etc/systemd/system/teletrans.service
   ```

2. Add the following content to the file:
   ```ini
   [Unit]
   Description=TeleTrans
   After=network.target

   [Service]
   Type=simple
   WorkingDirectory=/path/to/teletrans
   ExecStart=/usr/bin/python3 /path/to/teletrans/teletrans.py /path/to/your/directory
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```
   Replace `/path/to/teletrans` with the path to the project directory. `/path/to/your/directory` is the directory where the bot will store the configuration and logs.

3. Start the service and enable it to run on boot:
   ```sh
   sudo systemctl start teletrans
   sudo systemctl enable teletrans
   ```

4. Check the status of the service:
   ```sh
   sudo systemctl status teletrans
   ```

5. To stop the service, use:
   ```sh
   sudo systemctl stop teletrans
   ```

</details>

## Installation with Docker

<details>
   <summary>Click for Docker install details</summary>

1. Install Docker:
   ```sh
   bash <(curl -sSL https://get.docker.com)
   ```

2. Make a directory for the bot:
   ```sh
   mkdir teletrans
   cd teletrans
   ```

4. Create a `config.json` file in the project directory:
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

4. Run the bot with Docker:
   ```sh
   docker run -itd --name teletrans -v $(pwd):/app/config --restart=unless-stopped ghcr.io/ihategfw/teletrans:latest
   ```

5. For the first time, you need to execute the following command to log in to your Telegram account:
   ```sh
   docker exec -it teletrans python teletrans.py /app/config
   ```
   Follow the instructions to log in. 
   
   After logging in, please stop the container by pressing `Ctrl+C` and restart it:
   ```sh
   docker restart teletrans
   ```

</details>

## Usage

<details>
   <summary>Click for usage details</summary>

1. To enable translation from Chinese to English and Japanese, and keep the original message, use the following command in the chat:
   ```
   .tt-on,zh,zh|en|ja
   ```
   The code of languages supported by DeepL API can be found [here](https://developers.deepl.com/docs/resources/supported-languages).

2. To disable translation in the chat, simply use:
   ```
   .tt-off
   ```

3. To enable or disable global translation, use the following command:
   ```
   .tt-on-global,zh,zh|en|ja
   .tt-off-global
   ```
   - The chat config is prioritized over the global config.

4. If you want to send a message without translating it, use the `.tt-skip` command followed by your message:
   ```
   .tt-skip Hello, this message will not be translated.
   ```

5. Edited message is not translated by default. If you need to translate it, insert `.tt` at the beginning of the message.
   ```
   .tt This edited message will be translated.
   ```

6. If you want to translate the message you replied to, use the below command:
   ```
   .tt,zh,zh|en|ja
   ```

</details>

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MPL-2.0 License - see the [LICENSE](LICENSE) file for details.

