import aiohttp
import asyncio
import json
from icecream import ic
from config import (
    DOMAIN,
    CLIMATE_DATA,
    CLIMATE_METADATA,
    WEATHER_ALERTS,
                    )

CURRENTFILE = CLIMATE_DATA

# The URL you want to fetch data from
URL = f"{DOMAIN}{CURRENTFILE}"
ic(URL)

# OPT
# Headers that you want to include in your request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://opendata.chmi.cz/hydrology/now/data/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "If-Modified-Since": "Fri, 27 Sep 2024 15:00:09 GMT",
    "If-None-Match": '"66f6c879-1f75"',
    "Priority": "u=0, i"
}

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            # Check if the response status is OK (status code 200)
            if response.status == 200:
                data = await response.json()  # Parse JSON response
                return data
            else:
                return {"error": f"Failed to fetch data, status code: {response.status}"}

async def main():
    data = await fetch_data()
    ic(data)

    with open(CURRENTFILE.split('/')[-1], 'w') as json_file:
        json.dump(data,json_file)


# To run the async function
if __name__ == "__main__":
    asyncio.run(main())