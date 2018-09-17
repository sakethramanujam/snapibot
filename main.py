import discord
import requests
import os

TOKEN = os.environ['SNAPIBOT_TOKEN']

client = discord.Client()

@client.event
async def on_message(message):
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

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="https://www.spaceflightnewsapi.net"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
