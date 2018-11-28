"""
Contains the stuff for dealing with the r/SpaceX API
"""

import aiohttp


snapi_url = "https://api.spaceflightnewsapi.net/articles?limit=10"


async def latest_article():
    async with aiohttp.ClientSession() as session:
        async with session.get(snapi_url) as response:
            return await response.json()