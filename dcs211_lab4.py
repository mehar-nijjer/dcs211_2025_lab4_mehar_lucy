# dcs211_lab4.py

import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}

# Step 1: grabbing the file from my Lab4 folder
csv_path = "county_economic_status_2024.csv"

# Step 2: reading in the CSV but skipping the text at the top and bottom
arc_data = pd.read_csv(csv_path, skiprows=4, skipfooter=4, engine="python", thousands=",")

# Step 3: just checking that it loaded the way I want
print("\n=== First 10 rows of arc_data ===")
print(arc_data.head(10))

# Step 4: giving the columns shorter names so they’re easier to work with
arc_data.columns = [
    'fips',
    'state',
    'county',
    'arc_county',
    'col5',
    'col6',
    'pci',
    'poverty_rate',
    'avg_unemployment',
    # extras I’m not using right now
    'col10', 'col11', 'col12', 'col13', 'col14', 'col15'
]

print("\n=== Column names after renaming ===")
print(arc_data.columns)

# Step 5: dropping the first empty row (the one that has NaN for FIPS)
arc_data = arc_data.iloc[1:].reset_index(drop=True)

# Step 6: making sure the number columns are actually numeric
for col in ['poverty_rate', 'avg_unemployment', 'pci']:
    arc_data[col] = pd.to_numeric(arc_data[col], errors='coerce')

print("\n=== First 10 rows of arc_data after removing first row ===")
print(arc_data.head(10))

# printing out the poverty rate stats so I can see the averages and spread
print("\n=== Poverty Rate Summary (all counties) ===")
print("Mean:", arc_data['poverty_rate'].mean())
print("Standard deviation:", arc_data['poverty_rate'].std())
print("Min:", arc_data['poverty_rate'].min())
print("Max:", arc_data['poverty_rate'].max())

# Step 7: I wrote what mean and standard deviation mean in the Google Doc

# Step 8: checking what kind of object the 'state' column is
state_series = arc_data['state']
print("\nType of arc_data['state']:", type(state_series))


# Step 9: printing the number of counties per state
print("\n=== County Counts Per State ===")
state_counts = arc_data['state'].value_counts()
print(state_counts)

# Preparing aggregate arc_data (mean/median PCI and mean poverty) for state tables
state_summary = arc_data.groupby('state').agg(
    mean_pci=('pci', 'mean'),
    median_pci=('pci', 'median'),
    mean_poverty=('poverty_rate', 'mean')
)

# Combining county counts with summary stats
state_arc_data = pd.concat([state_counts.rename('num_counties'), state_summary], axis=1)

# Helper function to print state-level PrettyTables
def print_state_table(df: pd.DataFrame, title: str) -> None:
    """
    Formats and prints a tabular summary of state-level economic data.

    Parameters:
        df: A pandas DataFrame containing state-level data (e.g., mean PCI,
            poverty, or unemployment).
        title: The descriptive string title to be displayed above the table

    Returns:
        None
    """
    print(f"\n=== {title} ===")
    table = PrettyTable()
    table.field_names = ["State", "# counties", "PCI (mean)", "PCI (median)", "Poverty Rate (mean)"]

    for state, row in df.iterrows():
        table.add_row([
            state,
            int(row['num_counties']),
            f"{row['mean_pci']:.2f}",
            f"{row['median_pci']:.2f}",
            f"{row['mean_poverty']:.2f}"
        ])
    print(table)

# Step 10: Printing Top-Ten States
top_ten_states = state_arc_data.sort_values(by='num_counties', ascending=False).head(10)
print_state_table(top_ten_states, "10. Top-Ten States by Number of Counties")

# Step 11: Answer written in Google Doc

# Step 12: Print Bottom-Ten States (Excluding DC)
bottom_ten_states = state_arc_data[state_arc_data.index != 'District of Columbia'].sort_values(
    by='num_counties', ascending=True
).head(10)
print_state_table(bottom_ten_states, "12. Bottom-Ten States by Number of Counties (Excl. DC)")

# Step 13: Top-ten counties by decreasing poverty rate
top_ten_poverty_counties = arc_data.sort_values(by='poverty_rate', ascending=False).head(10)

print("\n=== 13. Top-Ten Counties by Decreasing Poverty Rate ===")
table = PrettyTable()
table.field_names = ["State", "County", "PCI", "Poverty Rate", "Avg Unemployment"]

for index, row in top_ten_poverty_counties.iterrows():
    table.add_row([
        row['state'],
        row['county'],
        f"{row['pci']:.2f}",
        f"{row['poverty_rate']:.2f}",
        f"{row['avg_unemployment']:.2f}"
    ])
print(table)

# Step 14: Flexible PrettyTable Function

def printTableBy(df: pd.DataFrame, field: str, how_many: int, title: str) -> None:
    """
    Prints a PrettyTable showing the top and bottom 'how_many' counties
    based on the specified field, with a divider in between.

    Parameters:
        df: The overall pandas arc_data frame.
        field: The column name (string) to select by (e.g., 'poverty_rate').
        how_many: The number of counties to include in the top and bottom lists.
        title: A string title to display before the table.

    Returns:
        None
    """
    print(f"\n=== 14. {title} ===")
    table = PrettyTable()
    table.field_names = ["State", "County", "PCI", "Poverty Rate", "Avg Unemployment"]

    # Top (Decreasing order)
    top_arc_data = df.sort_values(by=field, ascending=False).head(how_many)
    
    for _, row in top_arc_data.iterrows():
        table.add_row([
            f"{row['state']:<20}",
            f"{row['county']:<20}",
            f"{row['pci']:.2f}",
            f"{row['poverty_rate']:.2f}",
            f"{row['avg_unemployment']:.2f}"
        ])
    
    # Adding a separator
    table.add_row(["-"*20, "-"*20, "-"*8, "-"*14, "-"*16], divider=True)

    # Bottom (Increasing order)
    bottom_arc_data = df.sort_values(by=field, ascending=True).head(how_many)

    for _, row in bottom_arc_data.iterrows():
        table.add_row([
            f"{row['state']:<20}",
            f"{row['county']:<20}",
            f"{row['pci']:.2f}",
            f"{row['poverty_rate']:.2f}",
            f"{row['avg_unemployment']:.2f}"
        ])
    
    print(table)

# Calling the function for all three fields (Task 14 execution)
printTableBy(arc_data, 'poverty_rate', 10, "COUNTIES BY POVERTY RATE")
printTableBy(arc_data, 'avg_unemployment', 10, "COUNTIES BY AVERAGE UNEMPLOYMENT")
printTableBy(arc_data, 'pci', 10, "COUNTIES BY PER CAPITA INCOME")

# Step 16: Bar Plot Function

def createByStateBarPlot(df: pd.DataFrame, field: str, filename: str, title: str, y_label: str) -> None:
    """
    Creates a bar plot of the mean of a field, grouped by state, sorted ascending,
    with state abbreviations on the x-axis, and saves it to a file.

    Parameters:
        df: The pandas arc_data frame (ARC arc_data).
        field: The column name to select by (e.g., 'poverty_rate').
        filename: The string path to save the resulting figure (e.g., 'pov_rate.png').
        title: The string title for the plot.
        y_label: The string label for the y-axis.

    Returns:
        None
    """

    state_means = df.groupby('state')[field].mean().sort_values(ascending=True)

    state_abbreviations = state_means.index.map(lambda name: us_state_to_abbrev.get(name, name))
    state_means.index = state_abbreviations
    
    plt.figure(figsize=(12, 6))
    plt.bar(state_means.index, state_means.values)
    
    plt.title(title)
    plt.ylabel(y_label)
    plt.xticks(rotation=90, fontsize=8) 
    plt.grid(axis='y', alpha=0.5)
    plt.tight_layout() 
    plt.savefig(filename)
    plt.close() 

# Generating the three required images
createByStateBarPlot(arc_data, 'poverty_rate', "pov_rate.png", "States By Poverty Rate", "Poverty Rate")
createByStateBarPlot(arc_data, 'avg_unemployment', "unemployment.png", "States By Avg Unemployment", "Average Unemployment")
createByStateBarPlot(arc_data, 'pci', "pci.png", "States By Per Capita Income", "Per Capita Income")