from db import db
import asyncio


async def check_latest(client):
    await client.wait_until_ready()
    while not client.is_closed():
        result = db.newsnotifications.find({'send.discord': False})
        for document in result:
            print(document)
        await asyncio.sleep(10)

