import pandas as pd
from sqlalchemy import create_engine
import os

# Připojení k databázi přes SQLAlchemy
engine = create_engine('postgresql+psycopg2://postgres:postgres@meteodb.c3g80q0k67bi.us-east-1.rds.amazonaws.com:5432/MeteoDB')

# Načítání dat z CSV souboru
csv_file = './Data/2024120500_CLSHUMI_RELATIVE.csv'
df1 = pd.read_csv(csv_file)

# Načtení grid_points z databáze
grid_points = pd.read_sql("SELECT id AS grid_point_id, latitude, longitude FROM grid_points", engine)

# Připojení grid_point_id k df1 na základě latitude a longitude
df1 = df1.merge(grid_points, on=['latitude', 'longitude'], how='inner')

# Konverze date a time na datetime (předpokládáme, že jsou typu string)
df1['datetime'] = pd.to_datetime(
    df1['date'].astype(str) + df1['time'].astype(str),
    format='%Y%m%d%H%M'  # Formát odpovídá YYYYMMDD a HHMM
)

# Přičtení časového kroku (step) ve formě hodin
df1['datetime'] = df1['datetime'] + pd.to_timedelta(df1['step'], unit='h')

# Výběr názvu proměnné z názvu souboru
filename = os.path.basename(csv_file)  # Získání názvu souboru
variable_name = filename.split('_')[1]  # Například 'CLSHUMI_RELATIVE'
df1['variable_name'] = variable_name

# Zjištění, zda je proměnná již v tabulce 'phenomena'
phenomena_query = "SELECT id, name FROM phenomena WHERE name = %s"
existing_phenomenon = pd.read_sql(phenomena_query, engine, params=[variable_name])

# Pokud meteorologický jev neexistuje, přidáme nový záznam do tabulky 'phenomena'
if existing_phenomenon.empty:
    print(f"Meteorologický jev '{variable_name}' neexistuje v tabulce 'phenomena'. Přidávám nový záznam.")
    insert_query = "INSERT INTO phenomena (name, unit) VALUES (%s, %s)"
    # Pro příklad, nastavuji jednotku na '%', ale měla by být specifikována podle typu jevu
    engine.execute(insert_query, (variable_name, '%'))
    # Načteme nový id jevu
    existing_phenomenon = pd.read_sql(phenomena_query, engine, params=[variable_name])

phenomenon_id = existing_phenomenon['id'].iloc[0]

# Výběr relevantních sloupců pro tabulku 'observations'
observations = df1[['grid_point_id', 'variable_name', 'date', 'time', 'step', 'datetime', 'value']]
observations['phenomenon_id'] = phenomenon_id

# Odstranění duplicit na základě všech sloupců (chrání před opakovaným vložením stejných záznamů)
observations = observations.drop_duplicates()

# Získání již existujících záznamů v tabulce 'observations' pro porovnání
existing_observations = pd.read_sql("SELECT grid_point_id, datetime, value FROM observations", engine)

# Porovnání nových záznamů s již existujícími (detekce duplicit)
duplicates = pd.merge(observations, existing_observations, on=['grid_point_id', 'datetime', 'value'], how='inner')

# Pokud existují duplicity, vypiš hlášení o duplicitních záznamech
if not duplicates.empty:
    print(f"Bylo nalezeno {len(duplicates)} duplicitních záznamů. Tyto záznamy nebudou vloženy.")

# Záznamy, které nejsou duplicity
non_duplicates = observations[~observations.index.isin(duplicates.index)]

# Uložení dat do tabulky 'observations' bez přepsání stávajících dat
if not non_duplicates.empty:
    non_duplicates.to_sql('observations', engine, if_exists='append', index=False, method='multi')
    print(f"Záznamy byly úspěšně vloženy do tabulky 'observations'.")
else:
    print("Žádné nové záznamy k vložení.")
