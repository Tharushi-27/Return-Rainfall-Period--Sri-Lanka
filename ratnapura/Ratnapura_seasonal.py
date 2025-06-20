import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV (edit file name as needed)
df = pd.read_csv("C:/Users/DELL/Desktop/all district/ratnapura/CSV_Areal Rainfall Rathnapura.csv")

# Rename columns for easier handling
df.columns = ['Date', 'Rainfall', 'Month']

# Extract year for grouping
df['Year'] = df['Date'].str.slice(0, 4).astype(int)

# Define 4 seasons
season_dict = {
    'First Inter-Monsoon': [3, 4],
    'SW Monsoon': [5, 6, 7, 8, 9],
    'Second Inter-Monsoon': [10, 11],
    'NE Monsoon': [12, 1, 2]
}

plt.figure(figsize=(10, 6))

for season_name, months in season_dict.items():
    # Handle months crossing year boundary (Dec, Jan, Feb)
    if 12 in months:
        # Select rows where month in season, including December and Jan, Feb
        season_df = df[df['Month'].isin(months)]
    else:
        season_df = df[df['Month'].isin(months)]
    
    # Group by year → max rainfall per season
    yearly_max = season_df.groupby('Year')['Rainfall'].max().reset_index()
    
    # Rank data descending
    yearly_max = yearly_max.sort_values(by='Rainfall', ascending=False)
    yearly_max['Rank'] = range(1, len(yearly_max) + 1)
    N = len(yearly_max)
    yearly_max['Return Period'] = (N + 1) / yearly_max['Rank']
    
    # Plot
    plt.plot(yearly_max['Return Period'], yearly_max['Rainfall'], marker='o', label=season_name)

# Final plot settings

plt.xlabel('Return Period (years)')
plt.ylabel('Rainfall (mm)')
plt.title('Return Period vs Rainfall by Season (4 Seasons)')
plt.legend()
plt.grid(True, which='both', linestyle='--')
plt.tight_layout()
plt.show()
