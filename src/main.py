import argparse
import asyncio
from typing import Callable, Tuple, Union

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiohttp import web

from src.data.data_class.bot_data_class import BotConfig
from src.data.data_class.host_data_class import ServerConfig
from src.data.load_config import load_path
from src.handlers.callback import register_callback_handler
from src.handlers.massage import register_message_handler
from src.lib.anonymouse import AnonyMouse


class Service:
    bot: Bot
    dp: Dispatcher
    server_config: ServerConfig
    bot_config: BotConfig

    def __init__(self, load: Callable[[], Tuple[BotConfig, ServerConfig]],
                 stge: Union[MemoryStorage, RedisStorage2]):
        self.bot_config, self.server_config = load()
        self.bot = Bot(self.bot_config.token)
        self.dp = Dispatcher(self.bot, storage=stge)
        self.anonymouse = AnonyMouse()

    async def on_startup(self, web_app: web.Application):
        await self.bot.delete_webhook()
        await self.bot.set_webhook(self.server_config.get_url)

    def webhook(self, app: web.Application):
        app.on_startup.append(self.on_startup)
        app.add_routes([web.post(self.server_config.get_url, self.execute)])
        web.run_app(app, port=self.server_config.port, host=self.server_config.host)

    async def execute(self, req: web.Request) -> web.Response:
        updates = [types.Update(**(await req.json()))]
        Bot.set_current(self.dp.bot)
        Dispatcher.set_current(self.dp)
        try:
            await self.dp.process_updates(updates)
        except Exception as e:
            print(e)
        finally:
            return web.Response()

    async def main(self, build: str):
        register_message_handler(self.dp, self.bot)
        register_callback_handler(self.dp, self.bot, self.anonymouse)
        if build == "polling":
            print("start")
            await self.dp.start_polling()
        elif build == "webhook":
            app = web.Application()
            self.webhook(app)

    @staticmethod
    async def shutdown(dispatcher: Dispatcher):
        await dispatcher.storage.close()
        await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get arg')
    parser.add_argument("--config")
    parser.add_argument("--build")
    parser.add_argument("--storage")
    arg = parser.parse_args()
    path_to_data = "./data/data.json"
    storage = RedisStorage2() if arg.storage == "redis" else MemoryStorage()
    service = Service(load=load_path(arg.build, path=path_to_data), stge=storage)
    asyncio.run(service.main(arg.build))
