import asyncio
import os

import discord
import redis
from utils import spaceflightnewsapi

r = redis.Redis.from_url( os.environ['REDIS_URI'] )

async def send_latest(client):

    await client.wait_until_ready()
    while not client.is_closed:
        latest_article = await spaceflightnewsapi.latest_article()
        for article in latest_article:
            if article['_id'] != r.get('latest_id').decode():
                embed = discord.Embed(title=article['title'], description=article['news_site_long'],
                                      url=article['url'], color=2659031)
                embed.set_image(url=article['featured_image'])
                await client.send_message(client.get_channel(id='493854629747097610'), embed=embed) #TODO: Remove channel ID
                r.set('latest_id', article['_id'])
        await asyncio.sleep(10)


async def all_channels(client):
    await client.wait_until_ready()
    while not client.is_closed:
        for channel in client.get_all_channels():
            print(channel.id)
        await asyncio.sleep(60)
