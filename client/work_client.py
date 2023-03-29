import asyncio
from string import punctuation

from telethon import TelegramClient
from telethon import functions

from telethon.tl.types import InputPeerChannel, Message
from telethon.tl.functions.channels import JoinChannelRequest

from config_data.config import Config, load_config
from database.database import users_db


config: Config = load_config()
session = config.tg_client.tg_session
api_id = config.tg_client.api_id
api_hash = config.tg_client.api_hash






class ClientTg:
    def __init__(self, name: int, api_id: str, api_hash: str):
        self.user = name
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(str(name), api_id, api_hash)
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
    session: ClientTg = ClientTg(user_id, api_id, api_hash)
    await session.start()

    last_messages_of_chats: dict[str, int] = await session.create_dict_of_chats()
    count = 1
    while users_db[user_id]['work_on']:
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
            print(count, ':', users_db[user_id]['work_on'])
            count += 1
    await session.stop()
    print('ВЫХОД', user_id)






















# async def search_messages(channels: list[str], keywords: list[str], user: str, sleep: int = 10):
#     async with TelegramClient(session, api_id, api_hash) as client:
#         client: TelegramClient
#     await client.start()
#     count = 1
 
#     while users_db[user]['work_on']:

       
#         await asyncio.sleep(sleep)
#         print(count, ':', users_db[user]['work_on'])
#         count += 1

#     await client.disconnect


# async def search_messages(channels: list[str], keywords: list[str], user: str, sleep: int = 10):
#     asyncio.run(search(channels, keywords, user))
    

# import os
# import logging
# import sys
# import time
# from string  import punctuation
# import time



# from telethon.sync import TelegramClient
# from telethon import functions
# from telethon.tl.types import InputChannel, PeerChannel, InputPeerChannel
# from telethon.tl.functions.channels import JoinChannelRequest
# from telethon.tl.functions.messages import ImportChatInviteRequest

# from database.database import users_db




# session = "telethonClient"
# api_id = '20699084'
# api_hash = '0dde79f1f74cc07fee402e31f35d2cb4'
# my_id = '5628025616'


# client = TelegramClient(session, api_id, api_hash)


# def create_dict_of_chats(chats: list) -> dict:
#     """Cоздает словарь из списка чатов в формате: {id чата: id последнего сообщения}"""
#     chats = {key: find_id_last_message(key) for key in chats}
#     return chats


# def get_peer_by_id(chat_id):
#     return int(f"-100{chat_id}")


# def get_history_request(peer, limit_message):
#     # peer = get_peer_by_id(chat_id)
#     history = client(functions.messages.GetHistoryRequest(
#         peer=peer,
#         offset_id=0,
#         offset_date=None,
#         add_offset=0,
#         limit=limit_message,
#         max_id=0,
#         min_id=0,
#         hash=0
#     ))    
#     return history.messages


# def find_id_last_message(chat_id):
#     """Возвращает id последнего сообщения в чате"""
#     limit_message = 1
#     messages = get_history_request(chat_id, limit_message)
#     return messages[0].id


# def find_new_messages(chat_id, limit_message):
#     """Возвращает новые сообщения из чата"""
#     messages = get_history_request(chat_id, limit_message)
#     return messages 


# def messages_to_dict(messages):
#     all_messages = []
#     for message in messages:
#         all_messages.append(message.to_dict()) 
#     return all_messages


# def check_keywords(message: str, keywords: list) -> bool:
#     """Проверяет содержатся ли в сообщении ключевые слова"""
#     chars = punctuation
#     message = (s.lower().strip(chars) for s in message.split())

#     # res = any(item in message for item in keywords)
#     mes = set(message)
#     words = set(keywords)
#     res = (mes & words)
#     return bool(res)


# def forward_message(id_chat, message_id):
#     """Пересылает сообщение в чат"""
#     peer = get_peer_by_id(id_chat)
#     client(functions.messages.ForwardMessagesRequest(
#         from_peer=peer,
#         id=[message_id],
#         to_peer=my_id
#         ))


# def check_stop(fl=True):
#     return fl



# def search_messages(channels: list[str], keywords: list[str], user: str, sleep: int = 10):
#     client.start()
#     print('!!!!!!!!!!!!!!!!!!!!!')
#     keywords = ['продам', 'стол', 'стул', 'кресло']
#     peer_chats = [-1001806766676] # , 1537731683
#     time.sleep(2)
#     dict_chats = create_dict_of_chats(peer_chats)
#     # logger.debug(f' Создан словарь чатов для <пользователя> - {{id чата: id последнего сообщения в этом чате}}: \n{dict_chats}')
#     time.sleep(2)
#     print('сработала команда start')

#     dialogs = client.iter_dialogs()
#     for dialog in dialogs:
#         print(dialog.id, dialog.name)

    
#     while users_db[user]['work_on']:


#         time_update = 10
#         # logger.debug(f' Жду {time_update}c.')
#         sleep(time_update)
        

#         for id_chat, id_last_sent_mes in dict_chats.items():
#             id_last_message = find_id_last_message(id_chat)
#             sleep(1)
#             number_of_new_message = id_last_message - id_last_sent_mes
#             if number_of_new_message > 0:
#                 # logger.debug(' В <чате> найдены новые сообщения:')
#                 new_messages = find_new_messages(id_chat, number_of_new_message)
#                 all_messages = messages_to_dict(new_messages)
#                 dict_chats[id_chat] = id_last_message
#                 for message in all_messages:
#                     sleep(1)
#                     if message['message']:
#                         print('СООБЩЕНИЕ:', message['message'])
#                         if check_keywords(message['message'], keywords):
#                             # logger.debug(' СООБЩЕНИЕ ПОДХОДИТ!')
#                             forward_message(id_chat, new_messages[0].id)
#                             # logger.debug(f'сообщение переслано пользователю')
#                         else:
#                             print(' Cообщение не подходит.')
#             else:
#                 print(' Новых сообщений нет.')    
#     client.disconnect()


# # async def search_messages():
# #     try:
# #         print('(Press Ctrl+C to stop this)')
# #         try:
# #             await client.start()
# #             await client.run_until_disconnected(main())
# #         except KeyboardInterrupt:
# #             print(' Программа остановленна принудительно')
# #     finally:
# #         await client.disconnect()