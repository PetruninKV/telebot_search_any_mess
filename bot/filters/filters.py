import re

from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsListChannels(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[str]]:
        channels = []
        pattern = r'^https://t\.me/[\w_-]+$'
        for channel in message.text.split('\n'):
            if re.match(pattern, channel):
                channels.append(channel.strip())
        if channels:
            return {'channels': channels}
        return False

class IsListKeywords(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[str]]:
        keywords = []
        # print(message.text.split('\n'))
        for keyword in message.text.split('\n'):
            keywords.append(keyword.lower().strip())
        # print(keywords)
        if keywords:
            return {'keywords': keywords}
        return False
    

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        pass