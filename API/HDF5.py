import aiohttp
import asyncio
import bz2
from config import (
    DOMAIN,
    CLIMATE_DATA,
    CLIMATE_METADATA,
    WEATHER_ALERTS,
    WEATHER_RADAR_COMPOSITE_ECHOTOP,
)

CURRENTFILE = WEATHER_RADAR_COMPOSITE_ECHOTOP

# The URL you want to fetch data from
URL = f"{DOMAIN}{CURRENTFILE}"
ic(URL)

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            # Check if the response status is OK (status code 200)
            if response.status == 200:
                # Fetch the raw content as binary data
                data = await response.read()
                return data  # Return the compressed data
            else:
                # Handle the error case and return None
                ic(f"Failed to fetch data, status code: {response.status}")
                return None

async def main():
    # Await fetch_data to get the binary content
    data = await fetch_data()

    if data:
        file = CURRENTFILE.split('/')[-1]
        ic(f"File name: {file}")

        # Save the data
        with open(file, 'wb') as f:
            f.write(data)
            ic(f"HDF file saved as {file}")
    else:
        ic("Failed to fetch the data.")

# To run the async function
if __name__ == "__main__":
    asyncio.run(main())
