import asyncio

from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sessions import StringSession

from config_data.config import Config, load_config


config: Config = load_config()
api_id = config.tg_client.api_id
api_hash = config.tg_client.api_hash
session_string = config.tg_client.session_string


async def join_channels_request(channels: list) -> None | list[str]:
    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
        client: TelegramClient
        print('вход')
        error_join_channels = []
        await client.start()
        for link in channels:
            await asyncio.sleep(0.5)
            try:
                entity = await client.get_entity(link)
                await asyncio.sleep(0.1)
                peer = InputPeerChannel(entity.id, entity.access_hash)
                await asyncio.sleep(0.1)
                await client(JoinChannelRequest(peer))
                print(f'{entity.title} - запрос отправлен')
            except ValueError:
                print(f'Не получилось отправить запрос {entity.title}')
                error_join_channels.append(link)
                return error_join_channels
        await client.disconnect()
        print('выход')


