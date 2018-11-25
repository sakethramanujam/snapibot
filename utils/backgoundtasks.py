import asyncio
import os
import discord
import redis
import twitter
from utils import spaceflightnewsapi

r = redis.Redis.from_url(os.environ['REDIS_URL'])

api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
                  consumer_secret=os.environ['CONSUMER_SECRET'],
                  access_token_key=os.environ['ACCESS_TOKEN'],
                  access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])


async def send_latest(client):
    await client.wait_until_ready()
    while not client.is_closed:
        latest_article = await spaceflightnewsapi.latest_article()
        for article in latest_article:
            if article['_id'] == r.get('latest_id').decode():
                for subscribed_channel in r.lrange('subscribed_channels', 0, -1):
                    embed = discord.Embed(title=article['title'], description=article['news_site_long'],
                                          url=article['url'], color=2659031)
                    embed.set_image(url=article['featured_image'])
                    await client.send_message(client.get_channel(id=subscribed_channel.decode()), embed=embed)
                r.set('latest_id', article['_id'])
                api.PostUpdate('This is a test')
        await asyncio.sleep(10)
