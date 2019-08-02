from discord import Embed, Colour
from db import db
import asyncio


async def send_news_notification(client):
    await client.wait_until_ready()
    while not client.is_closed():

        result = db.newsnotifications.find({'send.discord': False})
        for document in result:
            channels = db.channels.find({"news": True})
            for i in channels:
                target = client.get_channel(i['channel'])
                embed = Embed(title=document['title'], url=document['url'], color=Colour(value=0x2196f3))
                embed.set_author(name=document['news_site_long'])
                embed.set_image(url=document['featured_image'])
                embed.set_footer(text="Powered by https://www.spaceflightnewsapi.net")
                await target.send(embed=embed)
            db.newsnotifications.update_one({'id': document['id']}, {"$set": {"send.discord": True}})

        await asyncio.sleep(10)


async def register_in_db(channel, topic):
    # Check if channel already exists in the db, and create one if it doesn't
    result = db.channels.count_documents({"channel": channel.id})
    if result == 0:
        db.channels.insert_one({"channel": channel.id, "news": False, "launches": False, "events": False})

    # Update channel with required topic
    if topic == "news":
        db.channels.update_one({"channel": channel.id}, {"$set": {"news": True}})


async def unregister(channel, topic):
    if topic == "news":
        db.channels.update_one({"channel": channel.id}, {"$set": {"news": False}})

    result = db.channels.find_one({"channel": channel.id})
    if result["events"] is False and result["launches"] is False and result["news"] is False:
        db.channels.delete_one({"channel": channel.id})
