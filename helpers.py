from db import db
import asyncio


async def check_latest(client):
    await client.wait_until_ready()
    while not client.is_closed():
        result = db.newsnotifications.find({'send.discord': False})
        for document in result:
            pass
        await asyncio.sleep(10)


async def register_in_db(channel, topic):
    # Check if we have permissions to write to this channel

    # Check if channel already exists in the db, and create one if it doesn't
    result = db.channels.count_documents({"channel": channel.id})
    if result == 0:
        db.channels.insert_one({"channel": channel.id, "news": False, "launches": False, "events": False})

    # Update channel with required topic
    if topic == "news":
        db.channels.update_one({"channel": channel.id}, {"$set": {"news": True}})
