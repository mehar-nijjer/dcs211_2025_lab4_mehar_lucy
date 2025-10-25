# dcs211_lab4.py
# Steps 1–8

import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# Step 1: grabbing the file from my Lab4 folder
csv_path = "county_economic_status_2024.csv"

# Step 2: reading in the CSV but skipping the text at the top and bottom
data = pd.read_csv(csv_path, skiprows=4, skipfooter=4, engine="python", thousands=",")

# Step 3: just checking that it loaded the way I want
print("\n=== First 10 rows of data ===")
print(data.head(10))

# Step 4: giving the columns shorter names so they’re easier to work with
data.columns = [
    'fips',
    'state',
    'county',
    'arc_county',
    'pci',
    'poverty_rate',
    'avg_unemployment',
    # extras I’m not using right now
    'col8', 'col9', 'col10', 'col11', 'col12', 'col13', 'col14', 'col15'
]

print("\n=== Column names after renaming ===")
print(data.columns)

# Step 5: dropping the first empty row (the one that has NaN for FIPS)
data = data[data['fips'].notna()].reset_index(drop=True)

# Step 6: making sure the number columns are actually numeric
for col in ['poverty_rate', 'avg_unemployment', 'pci']:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# printing out the poverty rate stats so I can see the averages and spread
print("\n=== Poverty Rate Summary (all counties) ===")
print("Mean:", data['poverty_rate'].mean())
print("Standard deviation:", data['poverty_rate'].std())
print("Min:", data['poverty_rate'].min())
print("Max:", data['poverty_rate'].max())

# Step 7: I wrote what mean and standard deviation mean in the Google Doc

# Step 8: checking what kind of object the 'state' column is
state_series = data['state']
print("\nType of data['state']:", type(state_series))
