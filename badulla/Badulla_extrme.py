import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
file_path = 'C:/Users/DELL/Desktop/all district/CSV_Extreme_Rainfall_By_Day_ratnapura.csv'
df = pd.read_csv(file_path)

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Extract Year and Month
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Filter only Southwest Monsoon months: May(5) to September(9)
df_monsoon = df[df['Month'].isin([5, 6, 7, 8, 9])]

# Define threshold for "extreme rainfall day" (you can change this!)
threshold = 105.0  # mm

# Filter only extreme rainfall days
df_extreme = df_monsoon[df_monsoon['Max_Rainfall'] > threshold]

# Find latest year
latest_year = df_extreme['Year'].max()
print(f"Latest year in Extreme Monsoon data: {latest_year}")

# Extract last 30 years
last_30_years = latest_year - 29
df_last30 = df_extreme[df_extreme['Year'] >= last_30_years]

# Count number of extreme days per year
extreme_days_count = df_last30.groupby('Year').size().reset_index(name='Extreme_Days')

# Plot
plt.figure(figsize=(12, 6))
plt.bar(extreme_days_count['Year'], extreme_days_count['Extreme_Days'], color='#c084fc')  # light purple

plt.title('Number of Extreme Rainfall Days during SW Monsoon (Last 30 Years) - Badulla')
plt.xlabel('Year')
plt.ylabel('Number of Extreme Rainfall Days')
plt.grid(axis='y')
plt.xticks(extreme_days_count['Year'], rotation=45)
plt.tight_layout()
plt.show()
