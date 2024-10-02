import aiohttp
import asyncio
from icecream import ic
from config import (
    CLIMATE_DATA,
    CLIMATE_METADATA,
    WEATHER_ALERTS,
)

CURRENTFILE = WEATHER_ALERTS

# The URL you want to fetch data from
URL = f"https://opendata.chmi.cz/{CURRENTFILE}"
ic(URL)

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            # Check if the response status is OK (status code 200)
            if response.status == 200:
                # Fetch the raw XML content as text (since it's XML)
                data = await response.text()
                return data
            else:
                return None, {"error": f"Failed to fetch data, status code: {response.status}"}

async def main():
    # Await fetch_data to get the content
    data = await fetch_data()

    if data:
        # Separate name of file from URL
        output_file = CURRENTFILE.split('/')[-1]
        ic(output_file)

        # Write the XML content directly to the file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(data)
            ic(f"Saved XML data to {output_file}")
    else:
        ic("Failed to fetch the XML data.")

# To run the async function
if __name__ == "__main__":
    asyncio.run(main())
