from pathlib import Path
from dataclasses import dataclass

from environs import Env

env_path = Path(__file__).parent.parent.parent.resolve() / "session settings" / ".env"


@dataclass
class TgBot:
    token: str

@dataclass
class TgClient:
    api_id: str
    api_hash: str
    session_string: str

# @dataclass
# class Admins:
#     ids: list(int)

@dataclass
class Config:
    tg_bot: TgBot
    tg_client: TgClient
    # id_admins: Admins


def load_config(path: str | None = None) -> Config:
    if not path:
        path = env_path
    env = Env()
    env.read_env(path)
    # admins = Admins(ids=[env.int(f'ADMIN_ID{i}') for i in range(1, 10)])
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')), 
                  tg_client=TgClient(api_id=env('TG_API_ID'),
                                     api_hash=env('TG_API_HASH'),
                                     session_string=env('TG_SESSION_STRING'))
                #   id_admins=admins
                  ) 

load_config(env_path)