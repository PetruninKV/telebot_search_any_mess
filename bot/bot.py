import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from config_data.config import Config, load_config
from key_boards.main_menu import set_main_menu
from handlers import other_handlers, pre_settings_handlers, client_handlers


logger = logging.getLogger(__name__)


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config()

    redis: Redis = Redis(host='redis')
    storage: RedisStorage = RedisStorage(redis=redis)

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)

    await set_main_menu(bot)

    dp.include_router(pre_settings_handlers.router)
    dp.include_router(client_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    try:
        asyncio.run(main())
        
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
