import asyncio
import time

import requests

import aiohttp

r = requests.get("https://flagcdn.com/fr/codes.json")
codes = r.json()


async def fetch(code, session):
    async with session.get(f"https://flagcdn.com/256x192/{code}.png") as resp:  # ②
        await resp.read()


async def main():
    t0 = time.time()

    async with aiohttp.ClientSession() as session:  # ②
        futures = [fetch(code, session) for code in codes]
        for response in await asyncio.gather(*futures):  # ①
            data = response

    print(f"fini: {time.time() - t0:.5f}s")


asyncio.run(main())
