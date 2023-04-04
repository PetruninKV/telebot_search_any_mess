import os
import sys
import time
from dotenv import load_dotenv, set_key


from telethon.sync import TelegramClient
from telethon.sessions import StringSession


def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)


load_dotenv()


api_id = get_env('TG_API_ID', 'Enter your API ID: ', int)
api_hash = get_env('TG_API_HASH', 'Enter your API hash: ')
bot_token = get_env('BOT_TOKEN', 'Enter your bot token: ')


with TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()

print(session_string)
set_key(".env", "TG_SESSION_STRING", session_string)
