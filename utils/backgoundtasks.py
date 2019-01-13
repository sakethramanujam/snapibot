import asyncio
import os
import discord
import redis
import tweepy
from utils import spaceflightnewsapi

r = redis.Redis.from_url(os.environ['REDIS_URL'])

auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)


async def send_latest(client):
    await client.wait_until_ready()
    while not client.is_closed:
        latest_articles = await spaceflightnewsapi.latest_article()
        for article in latest_articles:
            if r.sismember('latest_articles', article['_id']) is False:
                # for subscribed_channel in r.lrange('subscribed_channel', 0, -1):
                #     embed = discord.Embed(title=article['title'], description=article['news_site_long'],
                #                           url=article['url'], color=2659031)
                #     embed.set_image(url=article['featured_image'])
                #     await client.send_message(client.get_channel(id=subscribed_channel.decode()), embed=embed)
                r.sadd('latest_articles', article['_id'])
        await asyncio.sleep(60)


async def send_latest_twitter(client):
    await client.wait_until_ready()
    while not client.is_closed:
        latest_articles = await spaceflightnewsapi.latest_article()
        for article in latest_articles:
            if r.sismember('latest_articles_twitter', article['_id']) is False:
                # api.update_status('New article by %s: %s %s' % (article['news_site_long'], article['title'], article['url']))
                r.sadd('latest_articles_twitter', article['_id'])
        await asyncio.sleep(60)
