import eccodes as ec
import pandas as pd

def grib_to_csv(grib_file, csv_file):
    # Otevření GRIB souboru
    with open(grib_file, 'rb') as file:
        records = []
        while True:
            try:
                # Načtení další zprávy v GRIB souboru
                gid = ec.codes_grib_new_from_file(file)
                if gid is None:
                    break
                
                # Získání souřadnic a hodnot
                values = ec.codes_get_double_array(gid, 'values')
                lats, lons = ec.codes_get_double_array(gid, 'latitudes'), ec.codes_get_double_array(gid, 'longitudes')
                
                # Získání metadat (datum, čas, krok)
                date = ec.codes_get(gid, 'dataDate')
                time = ec.codes_get(gid, 'dataTime')
                step = ec.codes_get(gid, 'stepRange')

                # Ukládání dat
                for lat, lon, value in zip(lats, lons, values):
                    records.append({
                        'latitude': lat,
                        'longitude': lon,
                        'date': date,
                        'time': time,
                        'step': step,
                        'value': value
                    })
                
                # Uvolnění paměti pro aktuální zprávu
                ec.codes_release(gid)

            except ec.CodesInternalError:
                break

    # Vytvoření DataFrame a uložení do CSV
    df = pd.DataFrame(records)
    df.to_csv(csv_file, index=False)
    print(f"Data byla úspěšně uložena do {csv_file}")

# Volání funkce
grib_to_csv("./Data/2024120500_MSLPRESSURE.grb", "Data/2024120500_MSLPRESSURE.csv")
