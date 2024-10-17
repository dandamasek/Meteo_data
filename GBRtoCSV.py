import pygrib
import pandas as pd

# Open the GRIB file
grb_file = 'CLSW12.grb'
grbs = pygrib.open(grb_file)

# Initialize an empty list to store data from all messages
all_data = []

# Loop through all messages in the GRIB file
for grb in grbs:  
    # Extract latitudes, longitudes, and values for the current message
    lats, lons = grb.latlons()
    values = grb.values
    
    # Create a dictionary for the data
    data = {
        'Parameter Name:': grb.parameterName,
        'Units': grb.units,
        'ValidDate': grb.validDate,
        'Name': grb.shortName,
        'Latitude': lats.flatten(),
        'Longitude': lons.flatten(),
        'Value': values.flatten(),
    }
    print(grb)
    
    # Append the DataFrame for the current message to the list
    all_data.append(pd.DataFrame(data))
    #print(data)
    
# Concatenate all dataframes into a single one
df = pd.concat(all_data, ignore_index=True)


# Save the dataframe to a CSV file
df.to_csv('output.csv', index=False)

print("Conversion to CSV completed successfully!")
