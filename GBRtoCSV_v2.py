import os
import xarray as xr
import pandas as pd



# Define the folder where the GRIB files are stored
folder_path = 'Lamber_2.3km'

# List all GRIB files in the folder (files ending with .grb or .grb2)
grib_files = [f for f in os.listdir(folder_path) if f.endswith('.grb')]

all_data = []

# Loop through each GRIB file in the folder
for grib_file in grib_files:
    file_path = os.path.join(folder_path, grib_file)
    
    print(f"\nProcessing file: {grib_file}")
    
    # Open the GRIB file using xarray and cfgrib engine
    try:
        ds = xr.open_dataset(file_path, engine='cfgrib')
        
        #print(ds.variables['latitude'].values)
        #print(ds.variables['longitude'].values)
        print(ds.variables['valid_time'].values)

        data = {
        # 'Time': ds.variables['valid_time'].values,
        # 'Step': ds.variables['step'].values,
        # 'Latitude': ds.variables['latitude'].values,
        # 'Longtitude': ds.variables['longitude'].values,
        }

        all_data.append(pd.DataFrame(data))
        print(data)


    except Exception as e:
        print(f"Error processing {grib_file}: {e}\n")

df = pd.concat(all_data, ignore_index=True)

df.to_csv('output.csv', index=False)

print("Conversion to CSV completed successfully!")
