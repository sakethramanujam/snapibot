from discord import Embed, Colour
from discord.ext import commands
import urllib.request
import json

class Articles(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Articles cog loaded')

    @commands.command()
    async def latest(self, ctx):
        response = urllib.request.urlopen("https://www.spaceflightnewsapi.net/api/v1/articles?limit=5")
        response = response.read().decode()
        response = json.loads(response)

        for article in response['docs']:
            embed = Embed(title=article['title'], url=article['url'], color=Colour(value=0x2196f3))
            embed.set_author(name=article['news_site_long'])
            embed.set_image(url=article['featured_image'])
            embed.set_footer(text="Powered by https://www.spaceflightnewsapi.net")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Articles(client))

