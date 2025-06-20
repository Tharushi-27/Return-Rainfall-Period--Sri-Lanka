import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv('C:/Users/DELL/Desktop/all district/CSV_Extreme_Rainfall_By_Day_badulla.csv')

# Rename rainfall column if needed
df = df.rename(columns={'Max_Rainfall': 'Rainfall'})

# Convert Date column to datetime type
df['Date'] = pd.to_datetime(df['Date'])

# Extract year and month
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Define 4 seasons
season_dict = {
    'First Inter-Monsoon': [3, 4],
    'Southwest Monsoon': [5, 6, 7, 8, 9],
    'Second Inter-Monsoon': [10, 11],
    'Northeast Monsoon': [12, 1, 2]
}

plt.figure(figsize=(12, 7))

for season_name, months in season_dict.items():
    # Handle months that wrap across year boundary (Dec, Jan, Feb)
    if 12 in months:
        # Include December of previous year with Jan, Feb of current year
        season_df = df[(df['Month'].isin(months))]
    else:
        season_df = df[df['Month'].isin(months)]
    
    # Group by year and get max rainfall in that season
    yearly_max = season_df.groupby('Year')['Rainfall'].max().reset_index()
    
    # Sort descending rainfall to rank
    yearly_max = yearly_max.sort_values(by='Rainfall', ascending=False)
    
    # Calculate return period
    N = len(yearly_max)
    yearly_max['Rank'] = range(1, N + 1)
    yearly_max['Return Period'] = (N + 1) / yearly_max['Rank']
    
    # Plot Return Period vs Rainfall
    plt.plot(yearly_max['Return Period'], yearly_max['Rainfall'], marker='o', label=season_name)

plt.xscale('log')
plt.xlabel('Return Period (years)')
plt.ylabel('Rainfall (mm)')
plt.title('Return Period vs Rainfall by Season using daily rainfall data Colombo')
plt.legend()
plt.grid(True, which='both', linestyle='--')
plt.tight_layout()
plt.show()
