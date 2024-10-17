import aiohttp
import asyncio
import bz2
import os
from datetime import datetime
from config import (
    DOMAINLA,
    DOMAINCZ,
    SUBDOMAINCZ,
    ALADIN_ATTRIBUTES,
)

DOMAIN = DOMAINCZ
DIRNAME = "CZ"

# UTC HOUR
TIME = "12"


async def fetch_data(URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            # Check if the response status is OK (status code 200)
            if response.status == 200:
                # Fetch the raw content as binary data
                data = await response.read()
                return data  # Return only the data
            else:
                # Handle the error case and return None
                print(f"Failed to fetch data, status code: {response.status}")
                return None

async def main():
    # Format as YYYYMMDDTT where TT is time [00UTF,12UTF]
    current_date = datetime.now().strftime(f"%Y%m%d{TIME}")  

    # Cycle through all ALADIN_ATTRIBUTES
    for attribute in ALADIN_ATTRIBUTES:
        CURRENTFILE = f"{current_date}_{ALADIN_ATTRIBUTES[attribute]}.grb.bz2"

        # The URL you want to fetch data from
        URL = f"{DOMAIN}{TIME}{SUBDOMAINCZ}{CURRENTFILE}"
 

        # Await fetch_data to get the binary content
        data = await fetch_data(URL)

        if data:
            output_file_grb = CURRENTFILE.replace('.bz2', '')  # Change to .grb

            # Decompress the bz2 content
            try:
                decompressed_data = bz2.decompress(data)
            except Exception as e:
                print(f"Failed to decompress bz2 data: {e}")
                return

            # Create directory if it doesn't exist
            os.makedirs(f"{DIRNAME}", exist_ok=True)
            os.makedirs(f"{DIRNAME}/{TIME}", exist_ok=True)
            os.makedirs(f"{DIRNAME}/{TIME}/{current_date}", exist_ok=True)

            # Write the decompressed content (GRB file) to a new file
            with open(f"{DIRNAME}/{TIME}/{current_date}/" + output_file_grb, 'wb') as file:
                file.write(decompressed_data)
                print(f"Saved decompressed GRB data to {output_file_grb}\n")
        else:
            print("Failed to fetch the data.\n")

# To run the async function
if __name__ == "__main__":
    asyncio.run(main())
