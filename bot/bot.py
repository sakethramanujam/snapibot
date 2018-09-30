import discord
import requests
import os
import redis
from utils import backgoundtasks

# Settings
TOKEN = os.environ['SNAPIBOT_TOKEN']
r = redis.Redis.from_url(os.environ['REDIS_URL'])


class SpaceflightNewsAPI(discord.Client):

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author == client.user:
            return

        if message.content.startswith('!latest'):
            articles = requests.get('https://api.spaceflightnewsapi.net/articles?limit=5').json()
            for article in articles:
                embed = discord.Embed(title=article['title'], description=article['news_site_long'],
                                      url=article['url'], color=2659031)
                embed.set_image(url=article['featured_image'])
                await client.send_message(message.channel, embed=embed)

        if message.content.startswith('!info'):
            embed = discord.Embed(title="Spaceflight News API",
                                        description="Notifying on new space related news articles - "
                                                    "Powered by https://www.spaceflightnewsapi.net.", color=2659031)
            embed.add_field(name="Author", value="Derk Weijers")
            embed.add_field(name="Github ", value="https://github.com/spaceflightnewsapi/snapibot")
            await client.send_message(message.channel, embed=embed)

        if message.content.startswith('!help'):
            embed = discord.Embed(title="Spaceflight News API",
                                  description="Notifying on new space related news articles", color=2659031)
            await client.send_message(message.channel, embed=embed)

        if message.content.startswith('!register'):
            if message.author.server_permissions.administrator:
                if message.channel.id.encode() in r.lrange('subscribed_channels', 0, -1):
                    embed = discord.Embed(title="Oh no!",
                                          description="This channel is already registered!",
                                          color=2659031)
                    await client.send_message(message.channel, embed=embed)
                else:
                    r.lpush('subscribed_channels', message.channel.id)
                    embed = discord.Embed(title="This channel is now registered!",
                                      description="To unregister, issue \"!unregister\" in this channel", color=2659031)
                    await client.send_message(message.channel, embed=embed)
            else:
                embed = discord.Embed(title="Uh, Houston, we’ve had a problem",
                                      description="It seems like you're not a server admin. Please issue the command as admin!", color=2659031)
                await client.send_message(message.channel, embed=embed)

        if message.content.startswith('!unregister'):
            if message.author.server_permissions.administrator:
                if message.channel.id.encode() in r.lrange('subscribed_channels', 0, -1):
                    r.lrem('subscribed_channels', message.channel.id.encode())
                    embed = discord.Embed(title="This is SNAPI, signing off",
                                          description="This channel is now unregistered!",
                                          color=2659031)
                    await client.send_message(message.channel, embed=embed)
                else:
                    embed = discord.Embed(title="Ug oh!",
                                      description="This channel is currently not registered!", color=2659031)
                    await client.send_message(message.channel, embed=embed)
            else:
                embed = discord.Embed(title="Uh, Houston, we’ve had a problem",
                                      description="It seems like you're not a server admin. Please issue the command as admin!", color=2659031)
                await client.send_message(message.channel, embed=embed)

    async def on_ready(self):
        await client.change_presence(game=discord.Game(name="https://www.spaceflightnewsapi.net"))
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
        self.loop.create_task(backgoundtasks.send_latest(self))


client = SpaceflightNewsAPI()
client.run(TOKEN)
