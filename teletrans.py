# -*- coding: utf-8 -*-

import asyncio
import json
import logging
import os
import time
import sys

import aiohttp
import requests
from telethon import events
from telethon.sync import TelegramClient
from telethon.tl.types import MessageEntityBlockquote
from logging.handlers import RotatingFileHandler


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


async def translate_single(text, source_lang, target_lang, session):
    if source_lang == target_lang:
        return target_lang, text

    if target_lang == 'en' and openai_enable:
        url = openai_url
        headers = {
            "Authorization": "Bearer %s" % openai_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            'messages': [
                {
                'role': 'system',
                'content':'Your role is to be an English guru, an expert in authentic American English, who assists users in expressing their thoughts clearly and fluently. You are not just translating words; you are delving into the essence of the user message and reconstructing it in a way that maintains logical clarity and coherence. You will prioritize the use of plain English, short phrasal verbs, and common idioms. It is important to craft sentences with varied lengths to create a natural rhythm and flow, making the language sound smooth and engaging. Avoid regional expressions or idioms that are too unique or restricted to specific areas. Your goal is to make American English accessible and appealing to a broad audience, helping users communicate effectively in a style that resonates with a wide range of English speakers. No matter what I say, you only need to reply with the translated sentence.'
                },
                {
                'role': 'user',
                'content': text,
                }
            ],
            'stream': 'false',
            'model': openai_model,
            'temperature': 0.5,
            'presence_penalty': 0,
            'frequency_penalty': 0,
            'top_p': 1
        }

        start_time = time.time()
        async with session.post(url, headers=headers, data=json.dumps(payload)) as response:
            logger.info(f"翻译从 {source_lang} 至 {target_lang} 耗时: {time.time() - start_time}")
            response_text = await response.text()
            result = json.loads(response_text)
            try:
                return target_lang, result['choices'][0]['message']['content']
            except Exception as e:
                logger.error(f"OpenAI 翻译失败：{response_text}")
                
    url = "https://api.deeplx.org/translate"
    payload = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }

    start_time = time.time()
    async with session.post(url, json=payload) as response:
        logger.info(f"翻译从 {source_lang} 至 {target_lang} 耗时: {time.time() - start_time}")
        if response.status != 200:
            logger.error(f"翻译失败：{response.status}")
            raise Exception(f"翻译失败")

        result = await response.json()
        if result['code'] != 200:
            logger.error(f"翻译失败：{result}")
            raise Exception(f"翻译失败")

        return target_lang, result['data']


async def translate_text(text, source_lang, target_langs) -> {}:
    result = {}
    async with aiohttp.ClientSession() as session:
        tasks = [translate_single(text, source_lang, target_lang, session) for target_lang in target_langs]
        for lang, text in await asyncio.gather(*tasks):
            result[lang] = text

    return result


async def command_mode(event, target_key, text) -> bool:
    if text == '.tt-off':
        await event.delete()

        if target_key in target_config:
            del target_config[target_key]
            save_config()
            logger.info("已禁用: %s" % target_key)

        return False

    if text.startswith('.tt-on,'):
        await event.delete()

        _, source_lang, target_langs = text.split(',')
        target_config[target_key] = {
            'source_lang': source_lang,
            'target_langs': target_langs.split('|')
        }

        save_config()
        logger.info(f"设置成功: {target_config[target_key]}")

        return False

    if text.startswith('.tt-skip'):
        await event.message.edit(text[8:])
        logger.info("跳过翻译")
        return False

    return True

# 同时监听新消息事件和编辑消息事件，进行消息处理。
@client.on(events.NewMessage(outgoing=True))
@client.on(events.MessageEdited(outgoing=True))
async def handle_message(event):
    target_key = '%d.%d' % (event.chat_id, event.sender_id)
    try:
        message = event.message

        if not message.text:
            return

        message_content = message.text.strip()
        if not message_content:
            return

        # 判断event中是否包含entities，如果包含，则需要根据entities进行翻译。
        if message.entities:
            for entity in message.entities:
                if isinstance(entity, MessageEntityBlockquote):
                    return

        if message_content.startswith('.tt-') and not await command_mode(event, target_key, message_content):
            return

        if target_key not in target_config:
            return

        logger.info(f"翻译消息: {message.text}")

        config = target_config[target_key]
        target_langs = config['target_langs']
        if not target_langs:
            return

        start_time = time.time()  # 记录开始时间
        translated_texts = await translate_text(message.text, config['source_lang'], target_langs)
        logger.info(f"翻译耗时: {time.time() - start_time}")

        modified_message = translated_texts[target_langs[0]]

        if len(target_langs) > 1:
            secondary_messages = []
            for lang in target_langs[1:]:
                secondary_messages.append(translated_texts[lang])

            modified_message += '\n%s' % '\n'.join(secondary_messages)

        await client.edit_message(message, modified_message, formatting_entities=[MessageEntityBlockquote(offset=len(translated_texts[target_langs[0]])+1, length=len(modified_message)-len(translated_texts[target_langs[0]])-1)])

    except Exception as e:
        # 记录处理消息时发生的异常。
        logger.error(f"Error handling message: {e}")


# 启动客户端并保持运行。
try:
    client.start()
    client.run_until_disconnected()
finally:
    # 断开客户端连接。
    client.disconnect()