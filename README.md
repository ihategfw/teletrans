# TeleTrans - The Telegram Translator

TeleTrans is a Python-based Telegram bot that translates messages in real-time. It uses the OpenAI API and Google/Azure/DeepLX API for translation.


> [!WARNING]  
> This project requires the use of Telegram Apps API, which is a high-risk operation that could easily lead to a ban of your account. Please make sure you read and understand the [Telegram API Terms of Service](https://core.telegram.org/api/terms) before using this project.

## Features

- Real-time translation of messages.
- Supports multiple languages.
- Uses OpenAI/Gemini and Google/Azure/DeepLX for translation.
- Configurable source and target languages.
- Command mode for enabling/disabling translation and setting languages.

## Requirements

- Python 3.10-3.12

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

3. Create python virtual environments:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

5. Create a `config.json` file in the project directory:
    ```json
    {
      "api_id": "your_telegram_api_id",
      "api_hash": "your_telegram_api_hash",
      "translation_service": "deeplx",
      "google": {
         "creds": {}
      },
      "azure": {
         "key": "your_azure_key",
         "endpoint": "https://api.cognitive.microsofttranslator.com/",
         "region": "global"
      },
      "deeplx": {
         "url": "your_deeplx_url"
      },
      "openai": {
         "api_key": "your_openai_api_key",
         "url": "https://api.openai.com/v1/chat/completions",
         "model": "gpt-3.5-turbo",
         "prompt": "Translate the following text to tgt_lang: ",
         "temperature": 0.5
      },
      "gemini": {
         "api_key": "your_openai_api_key",
         "model": "gpt-3.5-turbo",
         "prompt": "Translate the following text to tgt_lang: ",
         "temperature": 0.5
      },
      "target_config": {}
   }
    ```
    - `api_id` and `api_hash` are required for the Telegram API. You can get them by creating a new application at [my.telegram.org](https://my.telegram.org).
    - `translation_service` can be set to `openai`, `google`, `azure` or `deeplx`
    - OpenAI/Gemini: You should keep the placeholder `tgt_lang` in the prompt.
    - Google: Click [here](https://cloud.google.com/translate/docs/setup) to create a Google Cloud project and get your Google Cloud credentials.
    - Azure: Click [here](https://learn.microsoft.com/en-us/azure/ai-services/translator/create-translator-resource) to create an Azure Translator resource and get your Azure key.
    - DeepLX: Click [here](https://linux.do/t/topic/111737) to get your unique API url.

6. Run the script with an optional argument to specify the working directory:
   ```sh
   python teletrans.py </path/to/your/directory>
   ```
   If no directory is specified, the script will run in the current directory.

7. After configuring everything, exit the venv.
   ```sh
   deactivate
   ```

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
   ExecStart=/path/to/teletrans/.venv/bin/python3 /path/to/teletrans/teletrans.py /path/to/your/directory
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

3. Create a `config.json` file in the project directory:
    ```json
    {
      "api_id": "your_telegram_api_id",
      "api_hash": "your_telegram_api_hash",
      "translation_service": "deeplx",
      "google": {
         "creds": {},
      },
      "azure": {
         "key": "your_azure_key",
         "endpoint": "https://api.cognitive.microsofttranslator.com/",
         "region": "global"
      },
      "deeplx": {
         "url": "your_deeplx_url"
      },
      "openai": {
         "api_key": "your_openai_api_key",
         "url": "https://api.openai.com/v1/chat/completions",
         "model": "gpt-3.5-turbo",
         "prompt": "Translate the following text to tgt_lang: ",
         "temperature": 0.5
      },
      "gemini": {
         "api_key": "your_openai_api_key",
         "model": "gpt-3.5-turbo",
         "prompt": "Translate the following text to tgt_lang: ",
         "temperature": 0.5
      },
      "target_config": {}
   }
    ```
    - `api_id` and `api_hash` are required for the Telegram API. You can get them by creating a new application at [my.telegram.org](https://my.telegram.org).
    - `translation_service` can be set to `openai`, `google`, `azure` or `deeplx`
    - OpenAI/Gemini: You should keep the placeholder `tgt_lang` in the prompt.
    - Google: Click [here](https://cloud.google.com/translate/docs/setup) to create a Google Cloud project and get your Google Cloud credentials.
    - Azure: Click [here](https://learn.microsoft.com/en-us/azure/ai-services/translator/create-translator-resource) to create an Azure Translator resource and get your Azure key.
    - DeepLX: Click [here](https://linux.do/t/topic/111737) to get your unique API url.

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

5. If you want to translate only this message once, use the following command, making sure to separate the command and the text with a space; this command ignores the `.tt-on` or `.tt-on-global` parameter:
   ```
   .tt-once,en,en|zh Hello, I am teletrans bot
   ```

6. Edited message is not translated by default. If you need to translate it, insert `.tt` at the beginning of the message.
   ```
   .tt This edited message will be translated.
   ```

7. If you want to translate the message you replied to, use the below command:
   ```
   .tt,zh,zh|en|ja
   ```

</details>

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MPL-2.0 License - see the [LICENSE](LICENSE) file for details.

