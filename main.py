import os
import sys
import time
from dotenv import load_dotenv

from telethon import TelegramClient, events


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

session = os.environ.get('TG_SESSION', 'printer')
api_id = get_env('TG_API_ID', 'Enter your API ID: ', int)
api_hash = get_env('TG_API_HASH', 'Enter your API hash: ')
bot_token = get_env('TOKEN', 'Enter your bot token: ')
proxy = None  

bot = TelegramClient(session, api_id, api_hash).start(bot_token=bot_token)




try:
    print('(Press Ctrl+C to stop this)')
    bot.run_until_disconnected()
finally:
    bot.disconnect()