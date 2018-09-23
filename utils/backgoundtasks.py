import asyncio
import redis
from utils import spaceflightnewsapi


async def send_latest(client):

    await client.wait_until_ready()
    while not client.is_closed:
        latest_article = await spaceflightnewsapi.latest_article()
        for article in latest_article:
            if article['_id'] == redis.get
        await client.send_message(client.get_channel(id='491221005117685771'), latest_article)
        await asyncio.sleep(10)