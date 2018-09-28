import asyncio
import os
import discord
import redis
from utils import spaceflightnewsapi

r = redis.Redis.from_url(os.environ['REDIS_URL'])


async def send_latest(client):
    await client.wait_until_ready()
    while not client.is_closed:
        latest_article = await spaceflightnewsapi.latest_article()
        for article in latest_article:
            if article['_id'] != r.get('latest_id').decode():
                for subscribed_channel in r.lrange('subscribed_channels', 0, -1):
                    embed = discord.Embed(title=article['title'], description=article['news_site_long'],
                                          url=article['url'], color=2659031)
                    embed.set_image(url=article['featured_image'])
                    await client.send_message(client.get_channel(id=subscribed_channel.decode()), embed=embed)
                r.set('latest_id', article['_id'])
        await asyncio.sleep(10)
