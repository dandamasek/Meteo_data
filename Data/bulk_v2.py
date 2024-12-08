import pandas as pd
from sqlalchemy import create_engine
import os
from tqdm import tqdm  # For progress bar
from config import engine

# Načítání dat z CSV souboru
csv_file = './Data/2024120500_MSLPRESSURE.csv'
df1 = pd.read_csv(csv_file)

# NAME 
start = csv_file.find('_')+1
name = csv_file[start:].split('.')[0]

# phenomena ID
phenomena = pd.read_sql("SELECT id AS phenomenon_id, name FROM phenomena", engine)
matching_phenomenon = phenomena[phenomena['name'] == name]
matching_phenomenon = matching_phenomenon["phenomenon_id"].iloc[0]
df1["phenomenon_id"] = matching_phenomenon

# get grid_point_id
grid_points = pd.read_sql("SELECT id AS grid_point_id, latitude, longitude FROM grid_points", engine)
df1 = df1.merge(grid_points, on=['latitude', 'longitude'], how='left')

observations = df1[['grid_point_id', 'phenomenon_id' ,'date', 'time', 'step', 'value']]

# Získání již existujících záznamů v tabulce 'observations' pro porovnání
existing_observations = pd.read_sql("SELECT grid_point_id, date, time, step, value FROM observations", engine)

# Porovnání nových záznamů s již existujícími (detekce duplicit)
duplicates = pd.merge(observations, existing_observations, on=['grid_point_id', 'value'], how='inner')

# Pokud existují duplicity, vypiš hlášení o duplicitních záznamech
if not duplicates.empty:
    print(f"Bylo nalezeno {len(duplicates)} duplicitních záznamů. Tyto záznamy nebudou vloženy.")

# Záznamy, které nejsou duplicity
non_duplicates = observations[~observations.index.isin(duplicates.index)]

# Procento úspěšně vložených záznamů
total_records = len(non_duplicates)
batch_size = 10000  # Nastavení velikosti dávky pro vložení (může se upravit)


# Uložení dat do tabulky 'observations' bez přepsání stávajících dat s progress bar
if total_records > 0:
    with tqdm(total=total_records, desc="Inserting records", unit="record") as pbar:
        for i in range(0, total_records, batch_size):
            # Vytvoření dávky záznamů
            batch = non_duplicates.iloc[i:i + batch_size]
            batch.to_sql('observations', engine, if_exists='append', index=False, method='multi')
            pbar.update(len(batch))  # Aktualizace progress baru s počtem záznamů v dávce
    print(f"Záznamy byly úspěšně vloženy do tabulky 'observations'.")
else:
    print("Žádné nové záznamy k vložení.")
