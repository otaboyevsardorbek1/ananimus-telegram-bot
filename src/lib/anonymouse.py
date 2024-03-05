import asyncio
from typing import Optional

import aiohttp

class AnonyMouse:
    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.api_link = "http://anonymouse.org/cgi-bin/anon-email.cgi"
        self.session = session or self.new_session()

    async def new_session(self) -> aiohttp.ClientSession:
        session = aiohttp.ClientSession()
        return session

    async def close(self) -> None:
        await self.session.close()

    async def send_email_message(self, mail: str, title: str, body: str) -> int:
        async with self.session.post(self.api_link, data={
            "to": mail,
            "subject": title,
            "text": body
        }) as response:
            return response.status

# Example usage:
async def main():
    anonymouse = AnonyMouse()
    status = await anonymouse.send_email_message("test@example.com", "Test Title", "Test Body")
    print(f"Email sent with status code: {status}")
    await anonymouse.close()

asyncio.run(main())
