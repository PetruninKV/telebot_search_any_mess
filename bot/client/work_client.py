import asyncio
from string import punctuation

from telethon import TelegramClient
from telethon import functions

from telethon.tl.types import Message
from telethon.sessions import StringSession

from config_data.config import Config, load_config
from database.database import users_db
from database import redis_db


config: Config = load_config()
api_id = config.tg_client.api_id
api_hash = config.tg_client.api_hash
session_string = config.tg_client.session_string


class ClientTg:
    def __init__(self, session_string: str, name: int, api_id: str, api_hash: str):
        self.user = name
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_string = session_string
        self.client = TelegramClient(StringSession(session_string), api_id, api_hash)
        self.peers = users_db[name]['list_channels']
        self.keywords = users_db[name]['list_keywords']

    async def start(self):
        await self.client.start()

    async def stop(self):
        await self.client.disconnect()

    async def get_history_request(self, peer=None, limit_message=1) -> list[Message]:
        await asyncio.sleep(0.5)
        history = await self.client(functions.messages.GetHistoryRequest(
            peer=peer,
            offset_id=0,
            offset_date=None,
            add_offset=0,
            limit=limit_message,
            max_id=0,
            min_id=0,
            hash=0
        ))    
        return history.messages

    async def find_id_last_message(self, peer):
        """Возвращает id последнего сообщения в чате"""
        limit_message = 1
        messages = await self.get_history_request(peer)
        return messages[0].id

    async def create_dict_of_chats(self) -> dict[str, int]:
        """Cоздает словарь из списка чатов в формате: {id чата: id последнего сообщения}"""
        chats = self.peers
        chats = {chat: await self.find_id_last_message(peer=chat) for chat in chats}
        return chats

    async def find_new_messages(self, chat, number_of_new_message):
        """Возвращает новые сообщения из чата"""
        messages = await self.get_history_request(peer=chat, limit_message=number_of_new_message)
        return messages 

    async def messages_to_dict(self, messages):
        all_messages = []
        for message in messages:
            all_messages.append(message.to_dict()) 
        return all_messages

    def check_keywords(self, message: str) -> bool:
        """Проверяет содержатся ли в сообщении ключевые слова"""
        chars = punctuation
        message = (s.lower().strip(chars) for s in message.split())
        # res = any(item in message for item in keywords)
        mes = set(message)
        words = set(self.keywords)
        res = (mes & words)
        return bool(res)

    async def forward_message(self, id_chat, message_id):
        """Пересылает сообщение в чат"""
        # peer = get_peer_by_id(id_chat)
        print('print id', message_id)
        await self.client(functions.messages.ForwardMessagesRequest(
            from_peer=id_chat,
            id=[message_id],
            to_peer=self.user
            ))
        print('Отправил')


async def search_messages(user_id):
    print('ВХОД', user_id)
    session: ClientTg = ClientTg(session_string, user_id, api_id, api_hash)
    await session.start()

    last_messages_of_chats: dict[str, int] = await session.create_dict_of_chats()
    count = 1
    while redis_db.get_status(user_id):
            for id_chat, id_last_sent_mes in last_messages_of_chats.items():
                id_last_message = await session.find_id_last_message(peer=id_chat)
                number_of_new_message = id_last_message - id_last_sent_mes
                if number_of_new_message > 0:
                    print('найдено новое сообщение:')
                    new_messages = await session.find_new_messages(id_chat, number_of_new_message)  
                    all_messages = await session.messages_to_dict(new_messages)
                    print(all_messages[0]['id'])
                    last_messages_of_chats[id_chat] = id_last_message
                    for message in all_messages:
                        if message['message']:
                            print(message['message'])
                            if session.check_keywords(message['message']):
                                await session.forward_message(id_chat, message['id'])
                            else:
                                print(' Cообщение не подходит.')                

            await asyncio.sleep(10)
            print(count, ':', 'work_on')
            count += 1
    print('work_off')
    await session.stop()
    print('ВЫХОД', user_id)