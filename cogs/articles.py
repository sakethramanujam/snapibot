from discord.ext import commands
import urllib.request
from discord import Embed, Colour
import json


class Articles(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Articles cog loaded')

    @commands.command()
    async def latest(self, ctx):
        if ctx == "news":
            response = urllib.request.urlopen("https://www.spaceflightnewsapi.net/api/v1/articles?limit=5")
            response = response.read().decode()
            response = json.loads(response)

            for article in response['docs']:
                embed = Embed(title=article['title'], url=article['url'], color=Colour(value=0x2196f3))
                embed.set_author(name=article['news_site_long'])
                embed.set_image(url=article['featured_image'])
                embed.set_footer(text="Powered by https://www.spaceflightnewsapi.net")
                await ctx.send(embed=embed)

        elif ctx == "launches":
            launches = urllib.request.urlopen("https://spacelaunchnow.me/api/3.3.0/launch/upcoming?limit=5")
            launches = response.read().decode()
            launches = json.loads(response)
            print(f'sending {ctx}')
            for launch in launches['results']:
                embed = Embed(title=launch['name'], color=Colour(value=0x2196f3))
                embed.set_image(url=launch['img_url'])
                embed.add_field(name='when', value=launch['net'], inline=False)
                embed.add_field(name='location', value=launch['pad']['location']['name'], inline=False)
                embed.set_footer(text="Powered by https://www.spacelaunchnow.me")
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Articles(client))
