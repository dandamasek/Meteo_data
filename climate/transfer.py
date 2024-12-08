import arcpy
arcpy.env.workspace = "C:/data"
arcpy.conversion.TableToGeodatabase(["stations_with_measurements.csv"], 
                                    "./output.gdb")