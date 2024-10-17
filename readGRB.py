# Import pygrib
import pygrib

# Open the GRIB2 file
grbs = pygrib.open('CLSW.grb')

# Loop through each GRIB message and print its forecast time and other metadata
for grb in grbs:
    print(f"Message: {grb.messagenumber}")
    print(f"  Parameter Name: {grb.parameterName}")
    print(f"  Units: {grb.units}")
    print(f"  Validity Date: {grb.validDate}")
    print(f"  Dimensions: {grb.values.shape}")
    print(f"  Grid Type: {grb.gridType}\n")

# Close the GRIB2 file
grbs.close()
