import aiohttp
import asyncio
import bz2
from icecream import ic
from config import (
    DOMAIN,
    CLIMATE_DATA,
    CLIMATE_METADATA,
    WEATHER_ALERTS,
    WEATHER_RADAR_COMPOSITE_ECHOTOP,
    WEATHER_NWP_ALADIN,
)

CURRENTFILE = WEATHER_NWP_ALADIN

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
                return data  # Return only the data
            else:
                # Handle the error case and return None
                ic(f"Failed to fetch data, status code: {response.status}")
                return None

async def main():
    # Await fetch_data to get the binary content
    data = await fetch_data()

    if data:
        output_file_bz2 = CURRENTFILE.split('/')[-1]
        ic(output_file_bz2)

        # Decompress the bz2 content
        try:
            decompressed_data = bz2.decompress(data)
        except Exception as e:
            ic(f"Failed to decompress bz2 data: {e}")
            return

        # Change the extension to .grb for the decompressed data
        output_file_grb = output_file_bz2.replace('.bz2', '')

        # Write the decompressed content (GRB file) to a new file
        with open(output_file_grb, 'wb') as file:
            file.write(decompressed_data)
            ic(f"Saved decompressed GRB data to {output_file_grb}")
    else:
        ic("Failed to fetch the data.")

# To run the async function
if __name__ == "__main__":
    asyncio.run(main())
