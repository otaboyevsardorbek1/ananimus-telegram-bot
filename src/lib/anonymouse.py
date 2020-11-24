import asyncio
from typing import Optional

import aiohttp


class AnonyMouse:
    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        """
        :param session:
        :return: None
        """
        self.api_link: str = "http://anonymouse.org/cgi-bin/anon-email.cgi"
        if session is None:
            asyncio.run(self.new_session())
            return
        self.session = session

    async def new_session(self) -> aiohttp.ClientSession:
        """
        :return:
        """
        self.session = aiohttp.ClientSession()
        return self.session

    async def close(self) -> None:
        """
        :return:  None
        """
        await self.session.close()

    async def send_email_message(self, mail: str, title: str, body: str) -> int:
        async with self.session.post(self.api_link, data={
            "to": mail,
            "subject": title,
            "text": body
        }) as response:
            return response.status
