# -*- coding: utf-8 -*-
import os
import time

import socks
from telethon import TelegramClient, events, sync

import tg_code

TG_PROXY = (socks.SOCKS5, "127.0.0.1", 7890)
CLIENT_TIMEOUT = 20
CLIENT_RETRIES = 2


def log(message):
    print("[pic_check] {}".format(message), flush=True)


def tg_qd(tg_bot, tg_command):
    log("{}: sending command {}".format(tg_bot, tg_command))
    client.send_message(tg_bot, tg_command)
    time.sleep(5)
    messages = client.get_messages(tg_bot)
    log("{}: latest reply: {}".format(tg_bot, messages[0].message))

    log("{}: downloading captcha image".format(tg_bot))
    messages[0].download_media(file="1.jpg")
    the_code = tg_code.truecaptcha()

    log("{}: sending captcha text {}".format(tg_bot, the_code))
    client.send_message(tg_bot, the_code)
    time.sleep(5)
    messages = client.get_messages(tg_bot)
    log("{}: latest reply: {}".format(tg_bot, messages[0].message))
    return messages[0].message


api_id = [int(os.environ["TELEGRAM_API_ID"])]
api_hash = [os.environ["TELEGRAM_API_HASH"]]
session_name = api_id[:]
bots_commands = ["@blueseamusic_bot", "/checkin", "鎴愬姛"]
for num in range(len(api_id)):
    session_name[num] = "id_" + str(session_name[num])
    log("starting session {}".format(session_name[num]))
    client = TelegramClient(
        session_name[num],
        api_id[num],
        api_hash[num],
        proxy=TG_PROXY,
        timeout=CLIENT_TIMEOUT,
        connection_retries=CLIENT_RETRIES,
    )
    client.start()
    log("session {} connected".format(session_name[num]))
    the_result = tg_qd(bots_commands[0], bots_commands[1])
    i = 0
    while bots_commands[2] not in the_result:
        i += 1
        log("{}: retry {}/5".format(bots_commands[0], i))
        the_result = tg_qd(bots_commands[0], bots_commands[1])
        if i > 5:
            log("{}: stopped after 5 retries".format(bots_commands[0]))
            break

os._exit(0)
