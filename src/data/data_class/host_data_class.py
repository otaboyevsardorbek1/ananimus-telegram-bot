import secrets
from dataclasses import dataclass


@dataclass
class ServerConfig:
    host: str
    port: int

    @property
    def get_url(self):
        return f"{self.host}/{secrets.token_urlsafe()}"
