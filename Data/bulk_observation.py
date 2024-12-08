import pandas as pd
from sqlalchemy import create_engine
import os
from tqdm import tqdm  # For progress bar

# Připojení k databázi přes SQLAlchemy
engine = create_engine('postgresql+psycopg2://postgres:postgres@meteodb.c3g80q0k67bi.us-east-1.rds.amazonaws.com:5432/MeteoDB')

# Načítání dat z CSV souboru
csv_file = './Data/2024112000_CLSWIND_SPEED.csv'
df1 = pd.read_csv(csv_file)

# Načtení grid_points z databáze
grid_points = pd.read_sql("SELECT id AS grid_point_id, latitude, longitude FROM grid_points", engine)
 
# Připojení grid_point_id k df1 na základě latitude a longitude
df1 = df1.merge(grid_points, on=['latitude', 'longitude'], how='inner')

# Přidání názvu proměnné (v tomto případě teploty)
filename = os.path.basename(csv_file)  # Získání názvu souboru
name = filename.split('_')[1]
df1['name'] = name

# Výběr relevantních sloupců pro tabulku 'observations'
observations = df1[['grid_point_id', 'name', 'date', 'time', 'step', 'value']]

# Odstranění duplicit na základě všech sloupců (chrání před opakovaným vložením stejných záznamů)
observations = observations.drop_duplicates()

# Získání již existujících záznamů v tabulce 'observations' pro porovnání
existing_observations = pd.read_sql("SELECT grid_point_id, datetime, value FROM observations", engine)

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
chunks = (total_records // batch_size) + 1  # Počet dávky

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
