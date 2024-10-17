import os
import xarray as xr
import pandas as pd

ds = xr.open_dataset('CLSW.grb', engine='cfgrib')
        
print(ds)