# -*- coding: utf-8 -*-

import asyncio
import json
import logging
import os
import time
import sys

import aiohttp
import requests
import re
from telethon import events
from telethon.sync import TelegramClient
from telethon.tl.types import MessageEntityBlockquote
from logging.handlers import RotatingFileHandler
import emoji


workspace = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

# 创建一个logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

# 创建一个handler，用于写入日志文件
handler = RotatingFileHandler('%s/log.txt' % workspace, maxBytes=20000000, backupCount=5)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(handler)

# 创建一个handler，用于输出到控制台
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(stream_handler)

def load_config():
    # load config from json file, check if the file exists first
    if not os.path.exists('%s/config.json' % workspace):
        logger.error('config.json not found, created an empty one')
        exit()

    with open('%s/config.json' % workspace, 'r') as f:
        config = json.load(f)

    return config


def save_config():
    cfg['target_config'] = target_config
    with open('%s/config.json' % workspace, 'w') as f:
        json.dump(cfg, f, indent=2)


cfg = load_config()
api_id = cfg['api_id']
api_hash = cfg['api_hash']
target_config = cfg['target_config'] if 'target_config' in cfg else {}
openai_config = cfg['openai'] if 'openai' in cfg else {}
openai_enable = openai_config['enable'] if 'enable' in openai_config else False
openai_api_key = openai_config['api_key'] if 'api_key' in openai_config else ''
openai_url = openai_config['url'] if 'url' in openai_config else 'https://api.openai.com/v1/chat/completions'
openai_model = openai_config['model'] if 'model' in openai_config else 'gpt-3.5-turbo'

# 初始化Telegram客户端。
client = TelegramClient('%s/client' % workspace, api_id, api_hash)
    
async def translate_text(text, source_lang, target_langs) -> {}:
    result = {}
    if emoji.purely_emoji(text):
        return result
    if source_lang == 'zh':
        # if text's first character is ascii
        if re.match(r'[a-zA-Z0-9]', text[0]):
            return result
    async with aiohttp.ClientSession() as session:
        tasks = []
        for target_lang in target_langs:
            if source_lang == target_lang:
                result[target_lang] = text
                continue
            if target_lang in ('en', 'ja') and openai_enable:
                    tasks.append(translate_openai(text, source_lang, target_lang, session))
            else:
                tasks.append(translate_deeplx(text, source_lang, target_lang, session))
        # 并发执行翻译任务。
        for lang, text in await asyncio.gather(*tasks):
            result[lang] = text

    return result

# 翻译deeplx API函数
async def translate_deeplx(text, source_lang, target_lang, session):
    url = "https://api.deeplx.org/MgYjqp0Y7JiclFY5nZ4dEnzMVAsXOuCmn_8iJVLIJBc/translate"
    payload = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }
    start_time = time.time()
    async with session.post(url, json=payload) as response:
        logger.info(f"DeepL 翻译从 {source_lang} 至 {target_lang} 耗时: {time.time() - start_time}")
        if response.status != 200:
            logger.error(f"翻译失败：{response.status}")
            raise Exception(f"翻译失败")

        result = await response.json()
        if result['code'] != 200:
            logger.error(f"DeepL翻译失败：{result}")
            raise Exception(f"DeepL翻译失败")

    return target_lang, result['data']

# 翻译openai API函数
async def translate_openai(text, source_lang, target_lang, session):
    url = openai_url
    headers = {
        "Authorization": "Bearer %s" % openai_api_key,
        "Content-Type": "application/json"
    }
    # 根据目标语言调整系统消息
    if target_lang == 'en':
        system_content = 'If my text cannot be translated or contains nonsencial content, just repeat my words precisely. As an American English expert, you\'ll help users express themselves clearly. You\'re not just translating, but rephrasing to maintain clarity. Use plain English and common idioms, and vary sentence lengths for natural flow. Avoid regional expressions. Respond with the translated sentence.'
    elif target_lang == 'ja':
        system_content = 'If my text cannot be translated or contains nonsencial content, just repeat my words precisely. As a Japanese language expert, you\'ll help users express themselves clearly. You\'re not just translating, but rephrasing to maintain clarity. Use plain Japanese and common idioms, and vary sentence lengths for natural flow. Avoid regional expressions. Respond with the translated sentence.'
    else:
        raise ValueError(f"Unsupported target language: {target_lang}")
    payload = {
        'messages': [
            {
            'role': 'system',
            'content': system_content
            },
            {
            'role': 'user',
            'content': text,
            }
        ],
        'stream': False,
        'model': openai_model,
        'temperature': 0.5,
        'presence_penalty': 0,
        'frequency_penalty': 0,
        'top_p': 1
    }

    start_time = time.time()
    async with session.post(url, headers=headers, data=json.dumps(payload)) as response:
        logger.info(f"OpenAI 翻译从 {source_lang} 至 {target_lang} 耗时: {time.time() - start_time}")
        response_text = await response.text()
        result = json.loads(response_text)
        try:
            return target_lang, result['choices'][0]['message']['content']
        except Exception as e:
            raise Exception(f"OpenAI 翻译失败：{response_text} {e}")

async def command_mode(event, target_key, text):
    if text.startswith('.tt-on-global') or text == '.tt-off-global':
        target_key = '0.%d' % event.sender_id
        text = text.replace('-global', '')

    if text == '.tt-off':
        await event.delete()
        if target_key in target_config:
            del target_config[target_key]
            save_config()
            logger.info("已禁用: %s" % target_key)
        return

    if text.startswith('.tt-on,'):
        _, source_lang, target_langs = text.split(',')
        if not source_lang or not target_langs:
            await event.message.edit("错误命令，正确格式: .tt-on,source_lang,target_lang1|target_lang2")
        else:
            target_config[target_key] = {
                'source_lang': source_lang,
                'target_langs': target_langs.split('|')
            }
            save_config()
            logger.info(f"设置成功: {target_config[target_key]}")
            await event.message.edit("设置成功: %s" % target_config[target_key])
        await asyncio.sleep(3)
        await event.message.delete()
        return

    if text.startswith('.tt-skip'):
        await event.message.edit(text[8:].strip())
        logger.info("跳过翻译")
        return

    if text.startswith('.tt-once,'):
        command, raw_text = text.split(' ', 1)
        _, source_lang, target_langs = command.split(',')
        logger.info(f"翻译消息: {raw_text}")
        await translate_and_edit(event.message, raw_text, source_lang, target_langs.split('|'))
        return

    await event.message.edit("未知命令")
    await asyncio.sleep(3)
    await event.message.delete()

# 同时监听新消息事件和编辑消息事件，进行消息处理。
@client.on(events.NewMessage(outgoing=True))
@client.on(events.MessageEdited(outgoing=True))
async def handle_message(event):
    target_key = '%d.%d' % (event.chat_id, event.sender_id)
    try:
        message = event.message
        # 忽略空消息。
        if not message.text:
            return
        message_content = message.text.strip()
        if not message_content:
            return

        # skip PagerMaid commands
        if message_content.startswith(','):
            return

        # skip bot commands
        if message_content.startswith('/'):
            return

        # command mode
        if message_content.startswith('.tt-'):
            await command_mode(event, target_key, message_content)
            return

        # handle reply message
        if message.reply_to_msg_id and message_content.startswith('.tt,'):
            _, source_lang, target_langs = message_content.split(',')
            logger.info(f"Reply message: {message.reply_to_msg_id}")
            reply_message = await client.get_messages(event.chat_id, ids=message.reply_to_msg_id)
            if not reply_message.text:
                return
            message_content = reply_message.text.strip()
            if source_lang and target_langs:
                logger.info(f"翻译消息: {message.text}")
                await translate_and_edit(message, message_content, source_lang, target_langs.split('|'))
            return

        # handle edited message
        if isinstance(event, events.MessageEdited.Event):
            if message_content.startswith('.tt'):
                message_content = message_content[3:].strip()
            else:
                return

        # chat config
        config = {}
        if target_key in target_config:
            config = target_config[target_key]
        else:
            # global config
            target_key = '0.%d' % event.sender_id
            if target_key not in target_config:
                return
            config = target_config[target_key]

        logger.info(f"翻译消息: {message.text}")
        source_lang = config['source_lang']
        target_langs = config['target_langs']
        await translate_and_edit(message, message_content, source_lang, target_langs)

    except Exception as e:
        # 记录处理消息时发生的异常。
        logger.error(f"Error handling message: {e}")

async def translate_and_edit(message, message_content, source_lang, target_langs):
    start_time = time.time()  # 记录开始时间
    translated_texts = await translate_text(message_content, source_lang, target_langs)
    logger.info(f"翻译耗时: {time.time() - start_time}")

    if not translated_texts:
        return

    modified_message = translated_texts[target_langs[0]]

    if len(target_langs) > 1:
        secondary_messages = []
        for lang in target_langs[1:]:
            secondary_messages.append(translated_texts[lang])

        modified_message += '\n%s' % '\n'.join(secondary_messages)

    # Handle special characters such as emojis and other unicode characters
    pattern = u'[\U00010000-\U0010ffff]'
    matches = len(re.findall(pattern, message_content))

    # Extract repeated computations
    translated_text = translated_texts[target_langs[0]]
    pattern_matches_translated = len(re.findall(pattern, translated_text))
    pattern_matches_modified = len(re.findall(pattern, modified_message))

    # Calculate offsets and lengths
    offset = len(translated_text) + pattern_matches_translated + 1
    length = len(modified_message) - len(translated_text) + pattern_matches_modified - pattern_matches_translated - 1

    # Create MessageEntityBlockquote with calculated values
    formatting_entities = [MessageEntityBlockquote(offset=offset, length=length)]

    # Edit the message
    await client.edit_message(message, modified_message, formatting_entities=formatting_entities)

# 启动客户端并保持运行。
try:
    client.start()
    client.run_until_disconnected()
finally:
    # 断开客户端连接。
    client.disconnect()