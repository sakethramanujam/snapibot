import asyncio
from utils import spaceflightnewsapi


async def send_latest(client):

    await client.wait_until_ready()
    while not client.is_closed():
        latest_article = await spaceflightnewsapi.latest_article()
        await client.send_message("491221005117685771", 'hoi')