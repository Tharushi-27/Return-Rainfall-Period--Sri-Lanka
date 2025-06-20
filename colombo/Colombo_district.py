import pandas as pd
import matplotlib.pyplot as plt

# Read CSV
df = pd.read_csv('C:/Users/DELL/Desktop/all district/colombo/CSV_Areal Rainfall Colombo.csv')  # change filename here

# Get rainfall column
rainfall_data = df['obs']

# Total number of months
N = len(rainfall_data)

# Sort rainfall descending
sorted_rainfall = rainfall_data.sort_values(ascending=False).reset_index(drop=True)

# Rank (i)
rank = sorted_rainfall.index + 1

# Return Period (in months)
return_period_months = (N + 1) / rank

# Return Period in years
return_period_years = return_period_months / 12

# Plot - swapped axes
plt.figure(figsize=(10, 6))
plt.plot(sorted_rainfall, return_period_years, marker='o', linestyle='-', color='green')

plt.xlabel('Rainfall (mm)')
plt.ylabel('Return Period (years)')
plt.title('Monthly Rainfall Return Period Plot for Ratnapura District (1951-2025)')
plt.grid(True)
plt.show()
