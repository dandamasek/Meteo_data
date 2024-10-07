import aiohttp
import asyncio
import bz2
from datetime import datetime
from icecream import ic
from config import (
   DOMAIN,
   ALADIN_ATTRIBUTES,
)



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
                ic(f"Failed to fetch data, status code: {response.status}")
                return None

async def main():
    # Format as YYYYMMDDTT where TT is time [00UTF,12UTF]
    from datetime import datetime
    current_date = datetime.now().strftime("%Y%m%d00")  
    print(current_date)

    # Cycle through all ALADIN_ATTRIBUTES
    for i in ALADIN_ATTRIBUTES:
        print(ALADIN_ATTRIBUTES[i])

        CURRENTFILE = f"{current_date}_{ALADIN_ATTRIBUTES[i]}.grb.bz2"
        ic(CURRENTFILE)

        # The URL you want to fetch data from
        URL = f"{DOMAIN}{CURRENTFILE}"
        ic(URL)

        # Await fetch_data to get the binary content
        data = await fetch_data(URL)

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
