import asyncio

from aiohttp import ClientSession
from eth_account import Account
from fake_useragent import FakeUserAgent as ua
from loguru import logger

import config

import random


def get_headers():
    return config.HEADERS.copy()


with open("mails.txt") as file:
    mails = file.readlines()


def get_mail(mails):
    random_mail = random.choice(mails).strip()
    index = mails.index(random_mail + "\n")
    mails.pop(index)
    return random_mail


async def join_whitelist(worker: str) -> None:
    while True:

        headers = get_headers()
        headers["User-Agent"] = ua().random

        async with ClientSession(headers=headers) as session:
            mail = get_mail(mails)
            resp = await session.post(
                "https://www.enclave.market/api/subscribe",
                json={
                    "email": mail,
                },
            )

        if resp.status == 200:
            logger.success(f"{worker} {mail}... - successfully registered!")
        else:
            logger.error(f"{worker} - {mail}... - {await resp.text()}")
            continue


async def main():
    await asyncio.gather(
        *[
            asyncio.create_task(join_whitelist(f"Worker {i+1}"))
            for i in range(config.THREADS)
        ]
    )
