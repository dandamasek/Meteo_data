import aiohttp
import asyncio
import bz2
import io
from datetime import datetime
from UploadFile import upload_file

from config import (
    DOMAINLA,
    DOMAINCZ,
    SUBDOMAINCZ,
    ALADIN_ATTRIBUTES,
    BUCKETNAME,
)

DOMAIN = DOMAINCZ
DIRNAME = "CZ"

# UTC HOUR
TIME = "00"

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

            #upload to AWS bucket
            file_in_memory = io.BytesIO(decompressed_data)
            upload_file(file_in_memory, BUCKETNAME, output_file_grb)

        else:
            print("Failed to fetch the data.\n")

# To run the async function
if __name__ == "__main__":
    asyncio.run(main())