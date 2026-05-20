# -*- coding: utf-8 -*-
import os
import sys
import time
from telethon import TelegramClient, events, sync
import tg_code

CLIENT_TIMEOUT = 20
CLIENT_RETRIES = 2


def log(message):
    text = "[telegram_check] {}".format(message)
    encoding = sys.stdout.encoding or "utf-8"
    print(text.encode(encoding, errors="replace").decode(encoding), flush=True)


class bot_check():
    def bot_pic(bot_id, messages):
        # client.send_message(bot_id, bot_command)  # 第一项是机器人ID，第二项是发送的文字
        # time.sleep(2)  # 延时2秒，等待机器人回应（一般是秒回应，但也有发生阻塞的可能）
        # messages = client.get_messages(bot_id)
        log("{}: downloading captcha image".format(bot_id))
        time.sleep(2)
        messages[0].download_media(file="1.jpg")
        the_code = tg_code.truecaptcha()
        log("{}: sending captcha text {}".format(bot_id, the_code))
        client.send_message(bot_id, the_code)
        time.sleep(5)
        messages = client.get_messages(bot_id)
        log("{}: latest reply: {}".format(bot_id, messages[0].message))
        return messages[0].message

    def bot_pic2(bot_id, bot_command):
        log("{}: retry with command {}".format(bot_id, bot_command))
        client.send_message(bot_id, bot_command)  # 第一项是机器人ID，第二项是发送的文字
        time.sleep(2)  # 延时5秒，等待机器人回应（一般是秒回应，但也有发生阻塞的可能）
        messages = client.get_messages(bot_id)
        time.sleep(2)
        log("{}: downloading captcha image".format(bot_id))
        messages[0].download_media(file="1.jpg")
        the_code = tg_code.truecaptcha()
        log("{}: sending captcha text {}".format(bot_id, the_code))
        client.send_message(bot_id, the_code)
        time.sleep(5)
        messages = client.get_messages(bot_id)
        log("{}: latest reply: {}".format(bot_id, messages[0].message))
        return messages[0].message

    def bot_inline(bot_id, messages):
        # client.send_message(bot_id, bot_command)  # 第一项是机器人ID，第二项是发送的文字
        # time.sleep(2)  # 延时5秒，等待机器人回应（一般是秒回应，但也有发生阻塞的可能）
        # messages = client.get_messages(bot_id)
        log("{}: downloading inline captcha image".format(bot_id))
        time.sleep(2)
        messages[0].download_media(file="1.jpg")
        time.sleep(2)
        the_code = tg_code.truecaptcha()

        log("{}: clicking inline button text {}".format(bot_id, the_code))
        res = messages[0].click(text=the_code)
        time.sleep(1)
        if str(res) == "None":
            log("{}: text button not found, clicking first button".format(bot_id))
            messages[0].click(0)
        time.sleep(5)
        messages = client.get_messages(bot_id)
        log("{}: latest reply: {}".format(bot_id, messages[0].message))
        return messages[0].message

    def bot_inline2(bot_id, bot_command):
        log("{}: retry with command {}".format(bot_id, bot_command))
        client.send_message(bot_id, bot_command)  # 第一项是机器人ID，第二项是发送的文字
        time.sleep(2)  # 延时5秒，等待机器人回应（一般是秒回应，但也有发生阻塞的可能）
        messages = client.get_messages(bot_id)
        time.sleep(2)
        log("{}: downloading inline captcha image".format(bot_id))
        messages[0].download_media(file="1.jpg")
        time.sleep(2)
        the_code = tg_code.truecaptcha()

        log("{}: clicking inline button text {}".format(bot_id, the_code))
        res = messages[0].click(text=the_code)
        time.sleep(1)
        if str(res) == "None":
            log("{}: text button not found, clicking first button".format(bot_id))
            messages[0].click(0)
        time.sleep(5)
        messages = client.get_messages(bot_id)
        log("{}: latest reply: {}".format(bot_id, messages[0].message))
        return messages[0].message


api_id = [int(os.environ["TELEGRAM_API_ID"])]
api_hash = [os.environ["TELEGRAM_API_HASH"]]
# bots_connands = {"@tsfsgkbot": ["/qd", "签到"], "@svipxddosbot": ["签到领积分", "成功"],"@pingansgk_bot": ["/qd", "签到"],"@HereisHopeBot": ["/sign", "每日签到"]}
# Old inactive bot list removed from runtime config.
# Disabled bots with no response or invalid usernames:
# @tsfsgkbot, @svipxddosbot, @pingansgk_bot, @HereisHopeBot, @aishegongkubot
bots_connands = {
    "@Zonesgk_bot": ["/qd", ""],
    "@Xray_E_Bot": ["/qd", ""],
    "@tianjigebot": ["/sign", ""],
    "@aisgk111111bot": ["📅 签到", ""],
    "@nb3344bot": ["/qd", ""],
    "@LSMCDLXBOT": ["📅 签到", ""],
}
def main():
    session_name = api_id[:]
    for num in range(len(api_id)):
        session_name[num] = "id_" + str(session_name[num])
        log("starting session {}".format(session_name[num]))
        client = TelegramClient(
            session_name[num],
            api_id[num],
            api_hash[num],
            timeout=CLIENT_TIMEOUT,
            connection_retries=CLIENT_RETRIES,
        )
        client.connect()
        if not client.is_user_authorized():
            raise RuntimeError("Telegram session is not authorized.")
        log("session {} connected".format(session_name[num]))
        for key, value in bots_connands.items():
            log("{}: sending command {}".format(key, value[0]))
            client.send_message(key, value[0])  # 第一项是机器人ID，第二项是发送的文字
            time.sleep(2)  # 延时5秒，等待机器人回应（一般是秒回应，但也有发生阻塞的可能）
            messages = client.get_messages(key)
            latest_message = messages[0].message or ""
            log("{}: latest reply: {}".format(key, latest_message))
            if value[1] not in latest_message:
                if messages[0].buttons != None:
                    log("{}: inline captcha detected".format(key))
                    i = 0
                    the_result = bot_check.bot_inline(key, messages)
                    while value[1] not in (the_result or ""):
                        time.sleep(10)
                        i += 1
                        log("{}: inline retry {}/5".format(key, i))
                        the_result = bot_check.bot_inline2(key, value[0])
                        if i >= 5:
                            log("{}: stopped after 5 retries".format(key))
                            break
                else:
                    log("{}: image captcha detected".format(key))
                    i = 0
                    the_result = bot_check.bot_pic(key, messages)
                    while value[1] not in (the_result or ""):
                        time.sleep(10)
                        i += 1
                        log("{}: image retry {}/5".format(key, i))
                        the_result = bot_check.bot_pic2(key, value[0])
                        if i >= 5:
                            log("{}: stopped after 5 retries".format(key))
                            break
            else:
                log("{}: success marker found, skipping captcha".format(key))


if __name__ == "__main__":
    main()
