from os import getenv
import orjson as json
from typing import Callable, Tuple

from src.data.data_class.bot_data_class import BotConfig
from src.data.data_class.host_data_class import ServerConfig


def load_path(build: str, path: str) -> Callable[[], Tuple[BotConfig, ServerConfig]]:
    if build == "evn":
        def load_evn() -> Tuple[BotConfig, ServerConfig]:
            token = getenv("token")
            host = getenv("host")
            port = getenv("port")
            return BotConfig(token=token), ServerConfig(host=host, port=port)

        return load_evn

    def load_json() -> Tuple[BotConfig, ServerConfig]:
        with open(path) as file:
            js = json.loads(file.read())
            bot = js["bot"]
            server = js["server"]
            return BotConfig(token=bot["token"]), ServerConfig(host=server["host"], port=server["port"])

    return load_json
