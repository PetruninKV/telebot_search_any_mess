import os
import logging
import sys
import time
from string  import punctuation
from dotenv import load_dotenv
from time import sleep


from telethon.sync import TelegramClient
from telethon import functions


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
my_id = 5628025616
        # Chat(-1001537731683),
        # Chat(-1001806766676),


client = TelegramClient(session, api_id, api_hash).start()


def create_dict_of_chats(chats: list) -> dict:
    """Cоздает словарь из списка чатов в формате: {id чата: id последнего сообщения}"""
    chats = {key: find_id_last_message(key) for key in chats}
    return chats


def get_peer_by_id(chat_id):
    return int(f"-100{chat_id}")


def get_history_request(chat_id, limit_message):
    peer = get_peer_by_id(chat_id)
    history = client(functions.messages.GetHistoryRequest(
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


def find_id_last_message(chat_id):
    """Возвращает id последнего сообщения в чате"""
    limit_message = 1
    messages = get_history_request(chat_id, limit_message)
    return messages[0].id


def find_new_messages(chat_id, limit_message):
    """Возвращает новые сообщения из чата"""
    messages = get_history_request(chat_id, limit_message)
    return messages 


def messages_to_dict(messages):
    all_messages = []
    for message in messages:
        all_messages.append(message.to_dict()) 
    return all_messages


def check_keywords(message: str, keywords: list) -> bool:
    """Проверяет содержатся ли в сообщении ключевые слова"""
    chars = punctuation
    message = (s.lower().strip(chars) for s in message.split())

    # res = any(item in message for item in keywords)
    mes = set(message)
    words = set(keywords)
    res = (mes & words)
    return bool(res)


def forward_message(id_chat, message_id):
    """Пересылает сообщение в чат"""
    peer = get_peer_by_id(id_chat)
    client(functions.messages.ForwardMessagesRequest(
        from_peer=peer,
        id=[message_id],
        to_peer=my_id
        ))


def check_stop(fl=True):
    return fl

def main():
    keywords = ['продам', 'стол', 'стул', 'кресло']
    id_chats = [1806766676] # , 1537731683
    sleep(2)
    dict_chats = create_dict_of_chats(id_chats)
    logger.debug(f' Создан словарь чатов для <пользователя> - {{id чата: id последнего сообщения в этом чате}}: \n{dict_chats}')
    sleep(2)
    print('сработала команда start')
    while True:


        time_update = 10
        logger.debug(f' Жду {time_update}c.')
        sleep(time_update)
        

        for id_chat, id_last_sent_mes in dict_chats.items():
            id_last_message = find_id_last_message(id_chat)
            sleep(1)
            number_of_new_message = id_last_message - id_last_sent_mes
            if number_of_new_message > 0:
                logger.debug(' В <чате> найдены новые сообщения:')
                new_messages = find_new_messages(id_chat, number_of_new_message)
                all_messages = messages_to_dict(new_messages)
                dict_chats[id_chat] = id_last_message
                for message in all_messages:
                    sleep(1)
                    if message['message']:
                        print('СООБЩЕНИЕ:', message['message'])
                        if check_keywords(message['message'], keywords):
                            logger.debug(' СООБЩЕНИЕ ПОДХОДИТ!')
                            forward_message(id_chat, new_messages[0].id)
                            logger.debug(f'сообщение переслано пользователю')
                        else:
                            logger.debug(' Cообщение не подходит.')
            else:
                logger.debug(' Новых сообщений нет.')    
        check = check_stop()
        if not check:
            break




if __name__ == '__main__':
    try:
        print('(Press Ctrl+C to stop this)')
        try:
            client.run_until_disconnected(main())
        except KeyboardInterrupt:
            logger.debug(' Программа остановленна принудительно')
    finally:
        client.disconnect()
























    # for dialog in client.iter_dialogs():
    #     if dialog.id in [-1001537731683, -1001806766676]:
    #         print(f"Getting history for chat {dialog.name} (ID: {dialog.id})")
    #         messages = client.iter_messages(dialog.id, limit=10)
    #         for message in messages:
    #             print(message.message)




# with TelegramClient(session, api_id, api_hash) as client:
#     result = client(functions.messages.GetChatsRequest(id=[-1001537731683]))
#     print(result.stringify())
#     print(result)



# @client.on(events.NewMessage(chats=[1806766676]))
# async def handle_new_message(event: events.newmessage.NewMessage.Event):
#     if 'хай' in event.message.message:
#         print('Найдено сообщение с ключевым словом:', event.message.message)
#         await client.forward_messages(entity=my_id, messages=event.message)
#         print(event.message.from_id)




# try:
#     print('(Press Ctrl+C to stop this)')
#     client.run_until_disconnected()
# finally:
#     client.disconnect()