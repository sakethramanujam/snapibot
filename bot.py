import discord
import os
from discord.ext import commands
from helpers import check_latest

client = commands.Bot(command_prefix='!')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.loop.create_task(check_latest(client))
client.run('NTk4NDkzOTgzODg2NTQwODAw.XSXdDA.gua_iudcsJ39tgD6i3WL6G6Rpio')
