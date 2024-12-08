import aiohttp
import asyncio
import csv
from collections import defaultdict

# The URLs you want to fetch data from
URL_1 = "https://opendata.chmi.cz/meteorology/climate/recent/metadata/meta1-20241101.json"
URL_2 = "https://opendata.chmi.cz/meteorology/climate/recent/metadata/meta2-20241101.json"

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": f"Failed to fetch data, status code: {response.status}"}

async def save_to_csv(data, filename="stations_with_measurements.csv"):
    # Access the station data from the first file
    header_1 = data[0]["data"]["data"]["header"].split(",")  # Parse the header string from the first file
    stations = data[0]["data"]["data"]["values"]  # Access station values from the first file
    
    # Access the measurement data from the second file
    header_2 = data[1]["data"]["data"]["header"].split(",")  # Parse the header string from the second file
    measurements = data[1]["data"]["data"]["values"]  # Access measurement values from the second file
    
    # Create a dictionary of measurements by WSI
    measurements_by_wsi = defaultdict(list)
    for measurement in measurements:
        wsi = measurement[1]  # WSI is the second item in each record
        eg_el_abbreviation = measurement[2]
        value = measurement[5]
        measurements_by_wsi[wsi].append((eg_el_abbreviation, value))

    # Prepare the header for the CSV
    extended_header = header_1.copy()
    extended_header.extend(["EG_EL_ABBREVIATION_" + str(i+1) for i in range(len(measurements_by_wsi[max(measurements_by_wsi.keys(), key=lambda k: len(measurements_by_wsi[k]))]))])
    extended_header.extend(["VALUE_" + str(i+1) for i in range(len(measurements_by_wsi[max(measurements_by_wsi.keys(), key=lambda k: len(measurements_by_wsi[k]))]))])

    # Write the merged data to CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(extended_header)  # Write the header

        # Merge the station data with the measurements by WSI
        for station in stations:
            wsi = station[0]
            row = station.copy()

            # Add measurements for the current station
            if wsi in measurements_by_wsi:
                for idx, (eg_el_abbreviation, value) in enumerate(measurements_by_wsi[wsi]):
                    row.append(eg_el_abbreviation)
                    row.append(value)

            # Fill missing columns if there are fewer measurements than the maximum
            if len(measurements_by_wsi[wsi]) < len(measurements_by_wsi[max(measurements_by_wsi.keys(), key=lambda k: len(measurements_by_wsi[k]))]):
                for _ in range(len(measurements_by_wsi[max(measurements_by_wsi.keys(), key=lambda k: len(measurements_by_wsi[k]))]) - len(measurements_by_wsi[wsi])):
                    row.append(None)
                    row.append(None)

            writer.writerow(row)  # Write the row

    print(f"Data saved to {filename}")

async def main():
    # Fetch both files
    data_1 = await fetch_data(URL_1)
    data_2 = await fetch_data(URL_2)

    # Check if both fetches were successful
    if "error" not in data_1 and "error" not in data_2:
        await save_to_csv([data_1, data_2])
    else:
        print(f"Error in fetching data: {data_1.get('error', '')} {data_2.get('error', '')}")

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
