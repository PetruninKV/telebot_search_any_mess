from telethon import TelegramClient

from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.channels import JoinChannelRequest

from config_data.config import Config, load_config





config: Config = load_config()
session = config.tg_client.tg_session
api_id = config.tg_client.api_id
api_hash = config.tg_client.api_hash




    
async def join_chats_request(channels: list) -> None | list[str]:
    async with TelegramClient(session, api_id, api_hash) as client:
        client: TelegramClient
        print('вход')
        error_join_channels = []
        await client.start()
        for link in channels:
            try:
                entity = await client.get_entity(link)
                peer = InputPeerChannel(entity.id, entity.access_hash)
                await client(JoinChannelRequest(peer))
                print(f'{entity.title} - запрос отправлен')
            except ValueError:
                print(f'Не получилось отправить запрос {entity.title}')
                error_join_channels.append(link)
                return error_join_channels
        await client.disconnect()
        print('выход')

