from environs import Env
from dataclasses import dataclass

@dataclass
class TgBot:
    token: str

@dataclass
class TgClient:
    tg_session: str
    api_id: str
    api_hash: str

@dataclass
class Config:
    tg_bot: TgBot
    tg_client: TgClient


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')), 
                  tg_client=TgClient(tg_session=env('TG_SESSION'), api_id=env('TG_API_ID'),api_hash=env('TG_API_HASH')))