import aiohttp


snapi_url = "https://spaceflightnewsapi.net/api/v1/articles?limit=10"


async def latest_article():
    async with aiohttp.ClientSession() as session:
        async with session.get(snapi_url) as response:
            articles = await response.json()
            return await articles['docs']