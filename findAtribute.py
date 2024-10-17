import os
import xarray as xr

# Define the folder where the GRIB files are stored
folder_path = 'Lamber_2.3km'

# List all GRIB files in the folder (files ending with .grb or .grb2)
grib_files = [f for f in os.listdir(folder_path) if f.endswith('.grb')]

# Loop through each GRIB file in the folder
for grib_file in grib_files:
    file_path = os.path.join(folder_path, grib_file)
    
    print(f"\nProcessing file: {grib_file}")
    
    # Open the GRIB file using xarray and cfgrib engine
    try:
        ds = xr.open_dataset(file_path, engine='cfgrib')
        
        # Display all available variables in the dataset
        print("Available variables in the GRIB file:")
        print(ds.variables)
        
    except Exception as e:
        print(f"Error processing {grib_file}: {e}\n")
