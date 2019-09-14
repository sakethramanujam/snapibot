import discord
import os
import helpers
from discord.ext import commands

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('Bot is ready.')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.author.send('Cannot register here - bot does not have required permissions!')

    if isinstance(error, commands.MissingPermissions):
        await ctx.author.send('You do not have the right permissions to do this')


@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.bot_has_permissions(send_messages=True)
@commands.has_permissions(administrator=True)
async def register(ctx, topic=""):
    if topic == "news":
        await helpers.register_in_db(ctx.channel, "news")
        await ctx.send("Registered for news")
    elif topic == "launches":
        await helpers.register_in_db(ctx.channel, "launches")
        await ctx.send("Registered for launches!")
    elif topic == "events":
        await ctx.send("Sorry, not implemented yet!")
    else:
        await ctx.send("Please provide a topic: news, launches, events")


@client.command()
@commands.has_permissions(administrator=True)
async def unregister(ctx, topic=""):
    if topic == "news":
        await helpers.unregister(ctx.channel, "news")
        await ctx.send("Unregistered for news")
    elif topic == "launches":
        await helpers.unregister(ctx.channel, "launches")
        await ctx.send("Unregistered for launches")
    elif topic == "events":
        await ctx.send("Sorry, not implemented yet!")
    else:
        await ctx.send("Please provide a topic: news, launches, events")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.loop.create_task(helpers.send_news_notification(client))
client.loop.create_task(helpers.send_launch_notification(client))
client.run(os.getenv('BOT_TOKEN'))